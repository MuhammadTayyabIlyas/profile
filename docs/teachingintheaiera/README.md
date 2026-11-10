# Teaching in the AI Era: book pages

Live at three URLs (served by nginx straight from this repo's folder, no build server):

- https://tayyabcheema.com/teachingintheaiera (book page)
- https://tayyabcheema.com/teachingintheaiera/read (reader: EPUB and PDF tabs)
- https://tayyabcheema.com/teachingintheaiera/references (482 references with a filter)

## Where things live

| What | Path on the server |
|---|---|
| Source files from the author (the `website/` folder) | `docs/teachingintheaiera-src/website/` |
| Files visitors download | `teachingintheaiera/files/` (`teaching-in-the-ai-era.epub`, `teaching-in-the-ai-era.pdf`, `teacher-workbook.pdf`, `teacher-workbook.docx`, `worksheets.pdf`, `cover.jpg`, `figures/`). `worksheets.pdf` is a byte copy of `teacher-workbook.pdf`, kept because the Kindle edition links to it; never delete it. The workbook PDFs carry 318 form fields: never compress, optimise or re-save them |
| Unpacked EPUB the reader loads chapter by chapter | `teachingintheaiera/read/book/` (generated; never edit by hand) |
| Page HTML and styles | `teachingintheaiera/index.html`, `references/index.html`, `read/index.html`, `book.css`, `read/reader.js` |
| Reader libraries (self-hosted) | `teachingintheaiera/read/lib/` (epub.js 0.3.93, PDF.js 3.11.174) |
| Resized images | `teachingintheaiera/img/` |
| Generator | `docs/teachingintheaiera/build_book.py` |
| nginx rules (clean URLs, gzip, EPUB type) | `/etc/nginx/sites-available/tayyabcheema.com.conf`, block starting `# Book: Teaching in the AI Era` |

## Online reading only (since 2026-11-10)

The book is sold as an ebook (Books2Read https://books2read.com/u/mdrgNO and KDP), so the site offers it to **read online only**:

- The full EPUB and PDF are never published. The builder reads the EPUB from `docs/teachingintheaiera-src/` to unpack it for the reader and deletes any published copy. nginx answers the old URLs `/teachingintheaiera/files/teaching-in-the-ai-era.{pdf,epub}` with a 301 to the book page. Both names are in `.gitignore`.
- The reader is EPUB-only: no PDF tab, no download button. Old `#pdf-N` links simply open the book.
- Still downloadable on purpose: the teacher's workbook (PDF, Word, and `worksheets.pdf` for the Kindle edition's link), the reference list page, and the citation files (BibTeX, `publications.bib`, CSL-JSON).
- nginx returns 404 for everything under `/docs/` (book sources, builders, interview notes). Before 2026-11-10 those paths were publicly readable.
- Online reading cannot stop a determined reader from copying the text; it only removes the easy download.

## Chapter landing pages (since 2026-11-10)

`/teachingintheaiera/introduction` and `/teachingintheaiera/chapter-1` … `chapter-13`: one page per chapter for search engines and backlinks. `build_book.py` generates them into `teachingintheaiera/chapters/*.html` from the unpacked EPUB: the opening paragraphs (whole paragraphs to about 120 words, never more than three), the chapter's own "This chapter…" paragraph when it has one, its section headings and its "Questions for reflection", all verbatim, plus Chapter and BreadcrumbList JSON-LD and sitemap entries. Never the full chapter: the book is sold. nginx maps the clean URLs (regex location before the `# Book` block) and 301s `/teachingintheaiera/chapters/*.html` to them. The book page's contents list links to these pages; the Last Word and the appendices still open in the reader.

The reader writes the current chapter into the address bar (`/read#ch005`), so a copied link opens that chapter; reloading your own chapter link resumes at the saved place.

## Replacing the EPUB and PDF for a new edition

1. Put the new files in `docs/teachingintheaiera-src/website/files/` with **exactly the same names**:
   `teaching-in-the-ai-era.epub`, `teaching-in-the-ai-era.pdf`, `teacher-workbook.pdf`, `teacher-workbook.docx`, `worksheets.pdf`.
   The builder sets each published file to mode 644; downloaders such as `gdown` save files owner-only, which nginx answers with 403.
   If the reference list changed, replace `docs/teachingintheaiera-src/website/references.md` too.
2. Run, from `/var/www/tayyabcheema.com`:
   ```
   python3 docs/teachingintheaiera/build_book.py
   ```
   It copies the three files into `teachingintheaiera/files/`, unpacks the EPUB into `read/book/` (swapped in one step, so a reader mid-chapter never sees half a book), rebuilds both reference lists, and stamps "Last updated" on all three pages.
3. Update the facts that live in the HTML by hand, if they changed:
   - page count and file sizes: `index.html` hero line (`EPUB 1.8 MB · PDF 3.4 MB, 239 pages`), the JSON-LD `numberOfPages`, and the homepage Research card (`Free to read, 239 pages`);
   - the edition stamp `ED` in `read/reader.js` (`?v=20261110`) and the matching `content.opf?v=` preload in `read/index.html`, then bump `reader.js?v=` there, so returning readers fetch the new book;
   - a new DOI version: search for `24085773` in `teachingintheaiera/` and `index.html`;
   - the contents list (19 parts) in `index.html` if chapters were added or renamed. Each item links to `/teachingintheaiera/read#chNNN`, the EPUB file name of that part.
4. Check: open the three URLs, open Chapter 1 in the reader, open the PDF tab and jump to a page.

Visitors' saved reading positions point into the old EPUB. If the chapters change a lot, bump the storage key in `read/reader.js` (`tiae-reader-v1` to `v2`, and the same key in the inline script in `read/index.html`) so everyone starts fresh instead of landing in the wrong place.

## Still to do (placeholders on the page)

- **Contact email**: done 2026-11-10, `update@pakedx.com` in the footer only (author's choice).
- **Paperback link**: done 2026-11-09, the hero button points at the Books2Read universal link https://books2read.com/u/mdrgNO (also a `Paperback` workExample in the JSON-LD). On that date Books2Read listed the ebook only; check that the paperback appears there.

## Deep links

- `/teachingintheaiera/read#ch003` opens Chapter 1 (`ch002` is the Introduction, `ch020` Appendix C).
- `/teachingintheaiera/read#pdf-112` opens the PDF at PDF page 112 (useful in citations: "PDF p. 112").
- `/teachingintheaiera/references#ref-25` highlights reference 25.
