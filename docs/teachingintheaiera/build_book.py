"""Publishes the book "Teaching in the AI Era" at /teachingintheaiera.

Run after replacing any file in SRC (see README.md in this folder):
    python3 docs/teachingintheaiera/build_book.py [path/to/website-folder]

It (1) copies the workbook (PDF and Word) and worksheets into /teachingintheaiera/files/
byte for byte (the workbook PDFs carry form fields), (2) unpacks the EPUB into
/teachingintheaiera/read/book/ for the in-browser reader. The book itself is sold, so its
EPUB and PDF are read from SRC and never published (nginx redirects the old URLs),
(3) rebuilds /teachingintheaiera/references/index.html from references.md and the
first-ten list on the book page, (4) writes one landing page per chapter at
/teachingintheaiera/introduction and /teachingintheaiera/chapter-N (opening, section list and
reflection questions, all verbatim from the EPUB; never the whole chapter) and adds them to
sitemap.xml, and (5) stamps "Last updated" on the book pages.
"""
import json
import datetime
import html
import re
import shutil
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "docs/teachingintheaiera-src/website"
BOOK = ROOT / "teachingintheaiera"
EPUB = SRC / "files" / "teaching-in-the-ai-era.epub"
FILES = ["worksheets.pdf", "teacher-workbook.pdf", "teacher-workbook.docx"]
UNPUBLISHED = ["teaching-in-the-ai-era.epub", "teaching-in-the-ai-era.pdf"]
LINK = re.compile(r"\[([^\]]+)\]\((https?://[^)\s]+)\)")
BARE = re.compile(r"(?<![\"'>])(https?://[^\s<]+[^\s<.,;)])")


def copy_files():
    for name in FILES:
        src = SRC / "files" / name
        if not src.exists():
            sys.exit(f"missing {src}")
        dst = BOOK / "files" / name
        shutil.copy2(src, dst)
        # sources can arrive owner-only (e.g. from a downloader); nginx must be able to read them
        dst.chmod(0o644)
    for name in UNPUBLISHED:
        (BOOK / "files" / name).unlink(missing_ok=True)


def unpack_epub():
    out = BOOK / "read" / "book"
    tmp = out.with_name("book.new")
    shutil.rmtree(tmp, ignore_errors=True)
    if not EPUB.exists():
        sys.exit(f"missing {EPUB}")
    with zipfile.ZipFile(EPUB) as z:
        for info in z.infolist():
            target = (tmp / info.filename).resolve()
            if not str(target).startswith(str(tmp.resolve())):
                sys.exit(f"unsafe path in EPUB: {info.filename}")
        z.extractall(tmp)
    # swap in one step so a reader mid-session never sees half a book
    old = out.with_name("book.old")
    shutil.rmtree(old, ignore_errors=True)
    if out.exists():
        out.rename(old)
    tmp.rename(out)
    shutil.rmtree(old, ignore_errors=True)
    # the reader opens EPUB/content.opf directly, so epub.js looks for Apple's
    # display options beside it; give it a copy rather than a 404
    opts = out / "META-INF" / "com.apple.ibooks.display-options.xml"
    if opts.exists():
        (out / "EPUB" / "META-INF").mkdir(exist_ok=True)
        shutil.copy2(opts, out / "EPUB" / "META-INF" / opts.name)


def entries():
    text = (SRC / "references.md").read_text(encoding="utf-8").replace("\r", "")
    paras = [p.strip() for p in text.split("\n\n") if p.strip()]
    return [p for p in paras if not p.startswith("#") and not p.startswith("*Teaching in the AI Era* cites")]


def entry_html(md):
    out, last = [], 0
    for m in LINK.finditer(md):
        out.append(html.escape(md[last:m.start()], quote=False))
        url = html.escape(m.group(2))
        out.append(f'<a href="{url}" target="_blank" rel="noopener">{html.escape(m.group(1), quote=False)}</a>')
        last = m.end()
    tail = html.escape(md[last:], quote=False)
    out.append(BARE.sub(lambda m: f'<a href="{m.group(1)}" target="_blank" rel="noopener">{m.group(1)}</a>', tail))
    return "".join(out)


def ref_list(items, start=1):
    return "\n".join(
        f'<li id="ref-{i}">{entry_html(e)}</li>' for i, e in enumerate(items, start)
    )


def replace_block(path, name, content):
    text = path.read_text(encoding="utf-8")
    pattern = re.compile(rf"(<!-- {name}:start -->)(.*?)(<!-- {name}:end -->)", re.S)
    if not pattern.search(text):
        sys.exit(f"marker {name} not found in {path}")
    path.write_text(pattern.sub(lambda m: f"{m.group(1)}\n{content}\n{m.group(3)}", text), encoding="utf-8")


# ---------- chapter landing pages ----------
SITE = "https://tayyabcheema.com"
BUY = "https://books2read.com/u/mdrgNO"
CHAPTERS = [("ch002", "introduction")] + [(f"ch{n + 2:03d}", f"chapter-{n}") for n in range(1, 14)]
KEEP = re.compile(r"</?(?:em|strong|i|b)>")


def inline(fragment):
    """Chapter HTML to page HTML: keep emphasis, drop links, spans and EPUB attributes."""
    fragment = re.sub(r"<(/?)(em|strong|i|b)\b[^>]*>", r"<\1\2>", fragment)
    return "".join(
        part if KEEP.fullmatch(part) else ("" if part.startswith("<") else part)
        for part in re.split(r"(<[^>]+>)", fragment)
    ).strip()


def plain(fragment):
    return html.unescape(re.sub(r"<[^>]+>", "", fragment)).strip()


def chapter_parts(xhtml):
    body = xhtml[xhtml.index("<h1"):]
    title = plain(re.search(r"<h1[^>]*>(.*?)</h1>", body, re.S).group(1))
    first_h2 = body.find("<h2")
    opening_html = body[:first_h2] if first_h2 > 0 else body
    paras = re.findall(r"<p>(.*?)</p>", opening_html, re.S)
    opening, words = [], 0
    for para in paras:
        if words >= 120 or len(opening) == 3:
            break
        opening.append(inline(para))
        words += len(plain(para).split())
    summary = next((inline(x) for x in paras[len(opening):]
                    if re.match(r"(This chapter|In this chapter)", plain(x))), None)
    sections = [plain(h) for h in re.findall(r"<h2[^>]*>(.*?)</h2>", body, re.S)]
    questions, intro = [], None
    if "Questions for reflection" in body:
        q = body[body.index("Questions for reflection"):]
        q = q[:q.index("</section>")] if "</section>" in q else q
        intro_m = re.search(r"</h2>\s*<p>(.*?)</p>", q, re.S)
        intro = inline(intro_m.group(1)) if intro_m else None
        ol = q[q.index("<ol"):q.index("</ol>")] if "<ol" in q else ""
        questions = [inline(li) for li in re.findall(r"<li>(?:<p>)?(.*?)(?:</p>)?</li>", ol, re.S)]
    desc_src = plain(summary) if summary else plain(paras[0])
    return title, opening, summary, sections, intro, questions, describe(desc_src)


def describe(text, limit=158):
    out = ""
    for sentence in re.split(r"(?<=[.?!’])\s+", text):
        if len(out) + len(sentence) + 1 > limit:
            break
        out = f"{out} {sentence}".strip()
    if not out:
        out = text[:limit].rsplit(" ", 1)[0] + "…"
    return out


def chapter_page(i, ch, slug, parts, prev, nxt, stamp, css):
    title, opening, summary, sections, intro, questions, desc = parts
    url = f"{SITE}/teachingintheaiera/{slug}"
    read = f"/teachingintheaiera/read#{ch}"
    short = title.split(". ", 1)[0]
    esc = lambda s: html.escape(s, quote=True)
    ld = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Chapter", "@id": f"{url}#chapter", "name": title, "url": url,
                "position": i, "description": desc, "inLanguage": "en-GB",
                "isPartOf": {"@type": "Book", "@id": f"{SITE}/teachingintheaiera#book", "name": "Teaching in the AI Era",
                             "isbn": "9798237344349", "url": f"{SITE}/teachingintheaiera"},
                "author": {"@type": "Person", "@id": f"{SITE}/#person", "name": "Muhammad Tayyab Ilyas"},
                "isAccessibleForFree": True,
                "potentialAction": {"@type": "ReadAction", "target": f"{SITE}{read}"},
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Teaching in the AI Era", "item": f"{SITE}/teachingintheaiera"},
                    {"@type": "ListItem", "position": 2, "name": short, "item": url},
                ],
            },
        ],
    }
    summary_html = f'\n        <h2 id="about-h">In this chapter</h2>\n        <p>{summary}</p>' if summary else ""
    sec_html = "\n".join(f"          <li>{esc(s)}</li>" for s in sections)
    q_html = ""
    if questions:
        items = "\n".join(f"          <li>{q}</li>" for q in questions)
        q_intro = f"\n        <p class=\"fine\">{intro}</p>" if intro else ""
        q_html = f"""
    <section class="sec alt" aria-labelledby="q-h">
      <div class="wrap prose">
        <h2 id="q-h">Questions for reflection</h2>{q_intro}
        <ol class="questions">
{items}
        </ol>
      </div>
    </section>
"""
    pager = []
    if prev:
        pager.append(f'<a rel="prev" href="/teachingintheaiera/{prev[0]}"><span>Previous</span>{esc(prev[1])}</a>')
    if nxt:
        pager.append(f'<a rel="next" href="/teachingintheaiera/{nxt[0]}"><span>Next</span>{esc(nxt[1])}</a>')
    page_title = f"{title} | Teaching in the AI Era"
    return f"""<!DOCTYPE html>
<html lang="en-GB">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{esc(page_title)}</title>
  <meta name="description" content="{esc(desc)}" />
  <meta name="author" content="Muhammad Tayyab Ilyas" />
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1" />
  <link rel="canonical" href="{url}" />
  <meta name="theme-color" content="#0A1C45" />
  <meta property="og:type" content="article" />
  <meta property="og:site_name" content="Muhammad Tayyab Ilyas" />
  <meta property="og:title" content="{esc(page_title)}" />
  <meta property="og:description" content="{esc(desc)}" />
  <meta property="og:url" content="{url}" />
  <meta property="og:image" content="{SITE}/teachingintheaiera/img/og-1200x627.jpg" />
  <meta property="og:image:width" content="1200" />
  <meta property="og:image:height" content="627" />
  <meta property="og:locale" content="en_GB" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:site" content="@TayyabCheema" />
  <meta name="twitter:title" content="{esc(page_title)}" />
  <meta name="twitter:description" content="{esc(desc)}" />
  <meta name="twitter:image" content="{SITE}/teachingintheaiera/img/og-1200x627.jpg" />
  <link rel="icon" type="image/x-icon" href="/favicon.ico" />
  <link rel="apple-touch-icon" href="/apple-touch-icon.png" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@600;700&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="/teachingintheaiera/book.css?v={css}" />
  <script type="application/ld+json">
{json.dumps(ld, ensure_ascii=False, indent=2)}
  </script>
</head>
<body>
  <a class="skip" href="#main">Skip to content</a>

  <header class="bar">
    <div class="wrap">
      <a href="/">Muhammad Tayyab Ilyas</a>
      <nav aria-label="Book">
        <a class="opt" href="/teachingintheaiera#contents">Contents</a>
        <a href="/teachingintheaiera/read">Read online</a>
      </nav>
    </div>
  </header>

  <main id="main">
    <section class="sec chapter-head" aria-labelledby="title">
      <div class="wrap prose">
        <nav class="crumbs" aria-label="Breadcrumb"><a href="/teachingintheaiera">Teaching in the AI Era</a> › <span aria-current="page">{esc(short)}</span></nav>
        <h1 id="title">{esc(title)}</h1>
        <p class="byline">From <a href="/teachingintheaiera"><i>Teaching in the AI Era</i></a> by Dr Muhammad Tayyab Ilyas</p>
        <div class="opening">
{chr(10).join(f"          <p>{x}</p>" for x in opening)}
        </div>
        <div class="btns">
          <a class="btn btn-primary" href="{read}">Read this chapter online</a>
          <a class="btn" href="{BUY}" rel="noopener">Buy the ebook</a>
        </div>{summary_html}
        <h2 id="sections-h">What the chapter covers</h2>
        <ul class="sections">
{sec_html}
        </ul>
      </div>
    </section>
{q_html}
    <section class="sec" aria-label="More chapters">
      <div class="wrap">
        <nav class="pager" aria-label="Chapters">{"".join(pager)}</nav>
      </div>
    </section>
  </main>

  <footer id="rights">
    <div class="wrap">
      <p>© 2026 Muhammad Tayyab Ilyas. All rights reserved.</p>
      <p>Contact: <a href="mailto:update@pakedx.com">update@pakedx.com</a></p>
      <p>Last updated {stamp}</p>
      <p><a href="/">tayyabcheema.com</a> · <a href="/teachingintheaiera">The book</a> · <a href="/teachingintheaiera/references">References</a> · <a href="/teachingintheaiera/read">Read online</a></p>
    </div>
  </footer>
</body>
</html>
"""


def build_chapters(stamp, today):
    css = re.search(r"book\.css\?v=(\d+)", (BOOK / "index.html").read_text(encoding="utf-8")).group(1)
    text = BOOK / "read" / "book" / "EPUB" / "text"
    parts = [chapter_parts((text / f"{ch}.xhtml").read_text(encoding="utf-8")) for ch, _ in CHAPTERS]
    out = BOOK / "chapters"
    out.mkdir(exist_ok=True)
    for i, ((ch, slug), p) in enumerate(zip(CHAPTERS, parts)):
        assert "—" not in "".join([p[0], p[6]]), f"em dash in {slug} metadata"
        prev = (CHAPTERS[i - 1][1], parts[i - 1][0]) if i else None
        nxt = (CHAPTERS[i + 1][1], parts[i + 1][0]) if i + 1 < len(CHAPTERS) else None
        page = chapter_page(i, ch, slug, p, prev, nxt, stamp, css)
        (out / f"{slug}.html").write_text(page, encoding="utf-8")
    sitemap = ROOT / "sitemap.xml"
    sm = sitemap.read_text(encoding="utf-8")
    for _, slug in CHAPTERS:
        loc = f"<loc>{SITE}/teachingintheaiera/{slug}</loc>"
        if loc in sm:
            sm = re.sub(rf"({re.escape(loc)}\s*<lastmod>)[^<]*", rf"\g<1>{today.isoformat()}", sm)
        else:
            sm = sm.replace("</urlset>", f"  <url>\n    {loc}\n    <lastmod>{today.isoformat()}</lastmod>\n  </url>\n</urlset>")
    sitemap.write_text(sm, encoding="utf-8")
    return len(CHAPTERS)


def main():
    copy_files()
    unpack_epub()
    refs = entries()
    today = datetime.date.today()
    stamp = f'<time datetime="{today.isoformat()}">{today.day} {today:%B %Y}</time>'
    pages = [BOOK / "index.html", BOOK / "references" / "index.html", BOOK / "read" / "index.html"]
    replace_block(pages[0], "first-refs", ref_list(refs[:10]))
    replace_block(pages[0], "ref-count", str(len(refs)))
    replace_block(pages[1], "all-refs", ref_list(refs))
    replace_block(pages[1], "ref-count", str(len(refs)))
    for p in pages:
        replace_block(p, "updated", stamp)
    n = build_chapters(stamp, today)
    print(f"published {len(FILES)} files, unpacked EPUB, {len(refs)} references, {n} chapter pages")


if __name__ == "__main__":
    main()
