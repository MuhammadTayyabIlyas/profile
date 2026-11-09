"""Publishes the book "Teaching in the AI Era" at /teachingintheaiera.

Run after replacing any file in SRC (see README.md in this folder):
    python3 docs/teachingintheaiera/build_book.py [path/to/website-folder]

It (1) copies the EPUB, PDF and worksheets into /teachingintheaiera/files/,
(2) unpacks the EPUB into /teachingintheaiera/read/book/ for the in-browser reader,
(3) rebuilds /teachingintheaiera/references/index.html from references.md and the
first-ten list on the book page, and (4) stamps "Last updated" on all three pages.
"""
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
FILES = ["teaching-in-the-ai-era.epub", "teaching-in-the-ai-era.pdf", "worksheets.pdf"]
LINK = re.compile(r"\[([^\]]+)\]\((https?://[^)\s]+)\)")
BARE = re.compile(r"(?<![\"'>])(https?://[^\s<]+[^\s<.,;)])")


def copy_files():
    for name in FILES:
        src = SRC / "files" / name
        if not src.exists():
            sys.exit(f"missing {src}")
        shutil.copy2(src, BOOK / "files" / name)


def unpack_epub():
    out = BOOK / "read" / "book"
    tmp = out.with_name("book.new")
    shutil.rmtree(tmp, ignore_errors=True)
    with zipfile.ZipFile(BOOK / "files" / FILES[0]) as z:
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
    print(f"published {len(FILES)} files, unpacked EPUB, {len(refs)} references")


if __name__ == "__main__":
    main()
