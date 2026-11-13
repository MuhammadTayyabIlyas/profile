"""Builds /publications/ (HTML), /publications/publications.bib, /publications/publications.json
(CSL-JSON) and docs/publications/llms-section.md (pulled into /llms.txt by docs/blog/build_blog.py).

Edit WORKS below (verified works only: never add anything not confirmed by the author), then run:
    python3 docs/publications/build_publications.py && python3 docs/blog/build_blog.py
"""
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SITE = "https://tayyabcheema.com"
ME = "Ilyas, Muhammad Tayyab"
ORCID = "https://orcid.org/0000-0002-5381-1996"
UPDATED = "2026-11-09"

WORKS = [
    {
        "key": "ilyas2026teaching", "group": "Book", "type": "book", "year": "2026",
        "authors": [ME], "title": "Teaching in the AI Era",
        "apa": "Ilyas, M. T. (2026). <em>Teaching in the AI era</em>. https://doi.org/10.5281/zenodo.24085773",
        "publisher": "Muhammad Tayyab Ilyas", "isbn": "9798237344349", "doi": "10.5281/zenodo.24085773",
        "url": f"{SITE}/teachingintheaiera",
        "summary": "A free book for school teachers, university staff and school leaders on AI in schools and universities: what the evidence shows, what it does not yet show, and what to do in a classroom with thirty students, one timetable and a weak connection.",
        "links": [("Read online", f"{SITE}/teachingintheaiera/read"),
                  ("Book page", f"{SITE}/teachingintheaiera"),
                  ("Buy the ebook", "https://books2read.com/u/mdrgNO"),
                  ("Buy the paperback", "https://www.amazon.com/s?k=Teaching+in+the+AI+Era+Muhammad+Tayyab+Ilyas&i=stripbooks")],
    },
    {
        "key": "ilyas2026scoping", "group": "Journal articles", "type": "article", "year": "2026",
        "authors": [ME, "Mercader, C.", "Bosco, A."],
        "title": "From technical literacy to AI-integrated pedagogy: A scoping review of digital competence frameworks for higher education (2000–2026)",
        "apa": "Ilyas, M. T., Mercader, C., &amp; Bosco, A. (2026). From technical literacy to AI-integrated pedagogy: A scoping review of digital competence frameworks for higher education (2000–2026). <em>The Turkish Online Journal of Educational Technology</em>, 25(4), 56–78.",
        "journal": "The Turkish Online Journal of Educational Technology", "volume": "25", "issue": "4", "pages": "56–78",
        "url": "https://www.tojet.net/articles/v25i4/2545.pdf",
        "links": [("Read or download PDF", "https://www.tojet.net/articles/v25i4/2545.pdf")],
    },
    {
        "key": "ilyas2026infrastructure", "group": "Journal articles", "type": "article", "year": "2026",
        "authors": [ME, "Mercader, C.", "Bosco, A."],
        "title": "Infrastructure-first digital competence in resource-constrained higher education",
        "apa": "Ilyas, M. T., Mercader, C., &amp; Bosco, A. (2026). Infrastructure-first digital competence in resource-constrained higher education. <em>Jurnal Pendidikan dan Profesi Keguruan (Progresif)</em>, 6(1), 77–91. https://doi.org/10.59562/progresif.v6i1.12473",
        "journal": "Jurnal Pendidikan dan Profesi Keguruan (Progresif)", "volume": "6", "issue": "1", "pages": "77–91",
        "doi": "10.59562/progresif.v6i1.12473",
        "links": [("Read online (DOI)", "https://doi.org/10.59562/progresif.v6i1.12473")],
    },
    {
        "key": "ilyas2026whatsapp", "group": "Journal articles", "type": "article", "year": "2026",
        "authors": [ME, "Mercader, C.", "Bosco, A."],
        "title": "WhatsApp as shadow learning management system: How university teachers in Pakistan build parallel pedagogical infrastructure under institutional prohibition",
        "apa": "Ilyas, M. T., Mercader, C., &amp; Bosco, A. (2026). WhatsApp as shadow learning management system: How university teachers in Pakistan build parallel pedagogical infrastructure under institutional prohibition. <em>ACADEMIA International Journal for Social Sciences</em>, 5(3b), 343–354. https://doi.org/10.63056/academia.5.3(b).2026.1779",
        "journal": "ACADEMIA International Journal for Social Sciences", "volume": "5", "issue": "3b", "pages": "343–354",
        "doi": "10.63056/academia.5.3(b).2026.1779", "license": "https://creativecommons.org/licenses/by/4.0/",
        "links": [("Read or download PDF", "https://academia.edu.pk/index.php/Journals/article/download/1779/2725"),
                  ("Article page (DOI)", "https://doi.org/10.63056/academia.5.3(b).2026.1779")],
    },
    {
        "key": "ilyas2023beliefs", "group": "Journal articles", "type": "article", "year": "2023",
        "authors": [ME, "Zaman, S."],
        "title": "An empirical enquiry into the teachers' philosophical beliefs and their actual classroom practices: A case of Pakistan",
        "apa": "Ilyas, M. T., &amp; Zaman, S. (2023). An empirical enquiry into the teachers' philosophical beliefs and their actual classroom practices: A case of Pakistan. <em>Journal of Positive School Psychology</em>, 7(4), 1843–1853.",
        "journal": "Journal of Positive School Psychology", "volume": "7", "issue": "4", "pages": "1843–1853",
        "url": "https://journalppw.com/index.php/jpsp/article/view/16914",
        "links": [("Read or download PDF", "https://journalppw.com/index.php/jpsp/article/download/16914/10703"),
                  ("Article page", "https://journalppw.com/index.php/jpsp/article/view/16914")],
    },
    {
        "key": "ilyas2026thesis", "group": "Doctoral thesis", "type": "thesis", "year": "2026",
        "authors": [ME],
        "title": "Exploring university teachers' pedagogical digital competence and its relationship with teaching practices",
        "apa": "Ilyas, M. T. (2026). <em>Exploring university teachers' pedagogical digital competence and its relationship with teaching practices</em> [Doctoral thesis, Universitat Autònoma de Barcelona]. TDX.",
        "school": "Universitat Autònoma de Barcelona", "url": "https://www.tdx.cat/handle/10803/698705",
        "links": [("Read on TDX (open access)", "https://www.tdx.cat/handle/10803/698705")],
    },
    {
        "key": "ilyas2026drives", "group": "Conference proceedings", "type": "inproceedings", "year": "2026",
        "authors": [ME, "Mercader Juan, C."],
        "title": "What drives successful technology integration? An examination of teacher digital competence through DigCompEdu in Pakistan",
        "apa": "Ilyas, M. T., &amp; Mercader Juan, C. (2026). What drives successful technology integration? An examination of teacher digital competence through DigCompEdu in Pakistan. In M. J. Bolarín Martínez &amp; A. Bernárdez Gómez (Eds.), <em>Libro de actas del XIV Congreso Iberoamericano de Docencia Universitaria</em> (pp. 320–321). Universidad de Santiago de Compostela.",
        "booktitle": "Libro de actas del XIV Congreso Iberoamericano de Docencia Universitaria",
        "editors": ["Bolarín Martínez, M. J.", "Bernárdez Gómez, A."], "pages": "320–321",
        "publisher": "Universidad de Santiago de Compostela",
        "url": "https://portalrecerca.uab.cat/en/publications/what-drives-successful-technology-integration-an-examination-of-t/",
        "links": [("UAB research portal record", "https://portalrecerca.uab.cat/en/publications/what-drives-successful-technology-integration-an-examination-of-t/")],
    },
    {
        "key": "ilyas2025caita", "group": "Software", "type": "software", "year": "2025",
        "authors": [ME], "title": "CAITA: Computer-Assisted Iterative Thematic Analysis",
        "apa": "Ilyas, M. T. (2025). <em>CAITA: Computer-Assisted Iterative Thematic Analysis</em> (Version 1) [Computer software]. Zenodo. https://doi.org/10.5281/zenodo.17474907",
        "publisher": "Zenodo", "version": "1", "doi": "10.5281/zenodo.17474907",
        "links": [("Zenodo (DOI)", "https://doi.org/10.5281/zenodo.17474907")],
    },
]
GROUPS = ["Book", "Journal articles", "Doctoral thesis", "Conference proceedings", "Software"]


def bib_escape(s):
    return s.replace("&", r"\&").replace("–", "--").replace("_", r"\_")


def bibtex(w):
    kind = {"book": "book", "article": "article", "thesis": "phdthesis", "inproceedings": "inproceedings", "software": "software"}[w["type"]]
    f = [("author", " and ".join(w["authors"])), ("title", "{" + w["title"] + "}" if w["type"] != "book" else "Teaching in the {AI} Era"), ("year", w["year"])]
    for k in ("journal", "booktitle", "volume", "pages", "school", "publisher", "version", "isbn"):
        if w.get(k):
            f.append((k, w[k]))
    if w.get("issue"):
        f.append(("number", w["issue"]))
    if w.get("editors"):
        f.append(("editor", " and ".join(w["editors"])))
    if w.get("doi"):
        f.append(("doi", w["doi"]))
    if w.get("url"):
        f.append(("url", w["url"]))
    body = ",\n".join(f"  {k} = {{{bib_escape(v) if k not in ('url', 'doi') else v}}}" for k, v in f)
    return f"@{kind}{{{w['key']},\n{body}\n}}"


def csl(w):
    def person(a):
        fam, _, giv = a.partition(", ")
        return {"family": fam, "given": giv}
    kind = {"book": "book", "article": "article-journal", "thesis": "thesis", "inproceedings": "paper-conference", "software": "software"}[w["type"]]
    item = {"id": w["key"], "type": kind, "title": w["title"], "author": [person(a) for a in w["authors"]],
            "issued": {"date-parts": [[int(w["year"])]]}}
    for src, dst in (("journal", "container-title"), ("booktitle", "container-title"), ("volume", "volume"), ("issue", "issue"),
                     ("pages", "page"), ("publisher", "publisher"), ("isbn", "ISBN"), ("doi", "DOI"), ("url", "URL"), ("version", "version")):
        if w.get(src):
            item[dst] = w[src]
    if w.get("school"):
        item["publisher"] = w["school"]
        item["genre"] = "Doctoral thesis"
    if w.get("editors"):
        item["editor"] = [person(e) for e in w["editors"]]
    return item


def jsonld(w):
    me = {"@id": f"{SITE}/#person"}
    others = [{"@type": "Person", "name": a} for a in w["authors"][1:]]
    t = {"book": "Book", "article": "ScholarlyArticle", "thesis": "Thesis", "inproceedings": "ScholarlyArticle", "software": "SoftwareSourceCode"}[w["type"]]
    d = {"@type": t, "name": w["title"], "author": [me] + others, "datePublished": w["year"]}
    if t == "Book":
        d["@id"] = f"{SITE}/teachingintheaiera#book"
    if w.get("doi"):
        d["sameAs"] = f"https://doi.org/{w['doi']}"
    if w.get("url"):
        d["url"] = w["url"]
    if w.get("isbn"):
        d["isbn"] = w["isbn"]
    if w.get("journal"):
        d["isPartOf"] = {"@type": "Periodical", "name": w["journal"]}
    if w.get("booktitle"):
        d["isPartOf"] = {"@type": "Book", "name": w["booktitle"]}
    if w.get("pages"):
        d["pagination"] = w["pages"]
    if w.get("school"):
        d["sourceOrganization"] = {"@type": "CollegeOrUniversity", "name": w["school"]}
    if w.get("license"):
        d["license"] = w["license"]
    return d


LEDE = ("Muhammad Tayyab Ilyas has published a book, <em>Teaching in the AI Era</em> (2026), four journal articles on "
        "teachers' digital competence and AI, a doctoral thesis at the Universitat Autònoma de Barcelona, a conference paper "
        "and the CAITA research software. Every entry has a DOI or publisher link and a BibTeX record.")


def page():
    graph = [{"@type": "Person", "@id": f"{SITE}/#person", "name": "Muhammad Tayyab Ilyas", "url": f"{SITE}/", "sameAs": [ORCID, "https://scholar.google.com/citations?user=z5OLA2sAAAAJ"]},
             {"@type": "CollectionPage", "@id": f"{SITE}/publications/#page", "url": f"{SITE}/publications/",
              "name": "Publications | Muhammad Tayyab Ilyas", "inLanguage": "en-GB", "dateModified": UPDATED,
              "about": {"@id": f"{SITE}/#person"},
              "mainEntity": {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "item": jsonld(w)} for i, w in enumerate(WORKS)]}}]
    sections = []
    for g in GROUPS:
        items = []
        for w in [w for w in WORKS if w["group"] == g]:
            links = "".join(f'<a href="{html.escape(u)}"{"" if u.startswith(SITE) else " target=\"_blank\" rel=\"noopener noreferrer\""}{" download" if u.endswith((".pdf", ".epub")) and u.startswith(SITE) else ""}>{t}</a>' for t, u in w["links"])
            summary = f'\n          <p class="pub-summary">{w["summary"]}</p>' if w.get("summary") else ""
            items.append(f'''        <li class="pub-item" id="{w['key']}">
          <p class="pub-cite">{w['apa']}</p>{summary}
          <p class="pub-links">{links}</p>
          <details class="pub-bib"><summary>BibTeX</summary><pre>{html.escape(bibtex(w))}</pre></details>
        </li>''')
        sections.append(f'      <h2 class="pub-group">{g}</h2>\n      <ol class="pub-list">\n' + "\n".join(items) + "\n      </ol>")
    css_v = (ROOT / "index.html").read_text().split("styles.css?v=")[1].split('"')[0]
    return f'''<!DOCTYPE html>
<html lang="en-GB">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Publications | Muhammad Tayyab Ilyas</title>
  <meta name="description" content="Publications by Muhammad Tayyab Ilyas: the book Teaching in the AI Era (2026), journal articles on teachers' digital competence and AI, a UAB doctoral thesis and the CAITA software. DOIs, PDFs and BibTeX." />
  <meta name="author" content="Muhammad Tayyab Ilyas" />
  <link rel="canonical" href="{SITE}/publications/" />
  <link rel="alternate" type="application/x-bibtex" title="All publications (BibTeX)" href="/publications/publications.bib" />
  <link rel="alternate" type="application/vnd.citationstyles.csl+json" title="All publications (CSL-JSON)" href="/publications/publications.json" />
  <meta property="og:type" content="website" />
  <meta property="og:title" content="Publications | Muhammad Tayyab Ilyas" />
  <meta property="og:description" content="The book Teaching in the AI Era, journal articles, a doctoral thesis and research software, with DOIs, PDFs and BibTeX." />
  <meta property="og:url" content="{SITE}/publications/" />
  <meta property="og:image" content="{SITE}/teachingintheaiera/img/og-1200x627.jpg" />
  <meta property="og:locale" content="en_GB" />
  <meta name="twitter:card" content="summary_large_image" />
  <link rel="icon" type="image/x-icon" href="/favicon.ico" />
  <link rel="apple-touch-icon" href="/apple-touch-icon.png" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Source+Sans+3:wght@400;600;700&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="/styles.css?v={css_v}" />
  <script type="application/ld+json">
{json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=2)}
  </script>
</head>
<body>
  <a class="skip-link" href="#main">Skip to content</a>
  <nav class="navbar" role="navigation" aria-label="Main navigation">
    <div class="container">
      <a href="/" class="nav-logo">Tayyab Ilyas</a>
      <button class="nav-toggle" aria-label="Toggle menu" aria-expanded="false">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5"/></svg>
      </button>
      <ul class="nav-links">
        <li><a href="/">Home</a></li>
        <li><a href="/teachingintheaiera">Book</a></li>
        <li><a href="/#research">Research</a></li>
        <li><a href="/blog/">Blog</a></li>
        <li><a href="/#contact" class="btn btn-primary">Contact</a></li>
      </ul>
    </div>
  </nav>
  <main id="main">
    <section class="case-hero">
      <div class="container">
        <p class="section-label">Research</p>
        <h1 class="case-hero-title">Publications</h1>
        <p class="case-hero-lede">{LEDE}</p>
        <p class="pub-links"><a href="/publications/publications.bib" download>Download all (BibTeX)</a><a href="/publications/publications.json" download>Download all (CSL-JSON)</a><a href="{ORCID}" target="_blank" rel="noopener noreferrer">ORCID</a><a href="https://scholar.google.com/citations?user=z5OLA2sAAAAJ&amp;hl=en" target="_blank" rel="noopener noreferrer">Google Scholar</a></p>
      </div>
    </section>
    <section class="case-section">
      <div class="container">
{chr(10).join(sections)}
        <p class="pub-meta" style="margin-top:2rem">Last updated {UPDATED}.</p>
      </div>
    </section>
  </main>
  <footer class="footer">
    <div class="container">
      <p class="footer-copy">&copy; 2026 Muhammad Tayyab Ilyas &middot; Barcelona, Spain</p>
    </div>
  </footer>
  <script src="/script.js?v={css_v}" defer></script>
</body>
</html>
'''


def llms_section():
    lines = ["## Publications", "",
             f"Full list with BibTeX: {SITE}/publications/ (machine-readable: {SITE}/publications/publications.bib and {SITE}/publications/publications.json). Cite with the APA references below.", ""]
    for w in WORKS:
        apa = w["apa"].replace("<em>", "*").replace("</em>", "*").replace("&amp;", "&")
        link = w["url"] if w["type"] == "book" else (f"https://doi.org/{w['doi']}" if w.get("doi") and w["doi"] not in apa else w.get("url", ""))
        lines.append(f"- {apa}" + (f" {link}" if link and link not in apa else ""))
    return "\n".join(lines) + "\n"


def main():
    out = ROOT / "publications"
    out.mkdir(exist_ok=True)
    text = page()
    assert "—" not in text, "em dash in publications page"
    (out / "index.html").write_text(text, encoding="utf-8")
    (out / "publications.bib").write_text("\n\n".join(bibtex(w) for w in WORKS) + "\n", encoding="utf-8")
    (out / "publications.json").write_text(json.dumps([csl(w) for w in WORKS], ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (ROOT / "docs/publications/llms-section.md").write_text(llms_section(), encoding="utf-8")
    print(f"built publications: {len(WORKS)} works")


if __name__ == "__main__":
    main()
