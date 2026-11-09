# Teaching in the AI Era: book pages

Live at three URLs (served by nginx straight from this repo's folder, no build server):

- https://tayyabcheema.com/teachingintheaiera (book page)
- https://tayyabcheema.com/teachingintheaiera/read (reader: EPUB and PDF tabs)
- https://tayyabcheema.com/teachingintheaiera/references (482 references with a filter)

## Where things live

| What | Path on the server |
|---|---|
| Source files from the author (the `website/` folder) | `docs/teachingintheaiera-src/website/` |
| Files visitors download | `teachingintheaiera/files/` (`teaching-in-the-ai-era.epub`, `teaching-in-the-ai-era.pdf`, `worksheets.pdf`, `cover.jpg`, `figures/`) |
| Unpacked EPUB the reader loads chapter by chapter | `teachingintheaiera/read/book/` (generated; never edit by hand) |
| Page HTML and styles | `teachingintheaiera/index.html`, `references/index.html`, `read/index.html`, `book.css`, `read/reader.js` |
| Reader libraries (self-hosted) | `teachingintheaiera/read/lib/` (epub.js 0.3.93, PDF.js 3.11.174) |
| Resized images | `teachingintheaiera/img/` |
| Generator | `docs/teachingintheaiera/build_book.py` |
| nginx rules (clean URLs, gzip, EPUB type) | `/etc/nginx/sites-available/tayyabcheema.com.conf`, block starting `# Book: Teaching in the AI Era` |

## Replacing the EPUB and PDF for a new edition

1. Put the new files in `docs/teachingintheaiera-src/website/files/` with **exactly the same names**:
   `teaching-in-the-ai-era.epub`, `teaching-in-the-ai-era.pdf`, `worksheets.pdf`.
   If the reference list changed, replace `docs/teachingintheaiera-src/website/references.md` too.
2. Run, from `/var/www/tayyabcheema.com`:
   ```
   python3 docs/teachingintheaiera/build_book.py
   ```
   It copies the three files into `teachingintheaiera/files/`, unpacks the EPUB into `read/book/` (swapped in one step, so a reader mid-chapter never sees half a book), rebuilds both reference lists, and stamps "Last updated" on all three pages.
3. Update the facts that live in the HTML by hand, if they changed:
   - page count and file sizes: `index.html` hero line (`EPUB 1.5 MB · PDF 3.2 MB, 238 pages`), the JSON-LD `numberOfPages`, and the homepage Research card (`Free to read, 238 pages`);
   - a new DOI version: search for `24085773` in `teachingintheaiera/` and `index.html`;
   - the contents list (19 parts) in `index.html` if chapters were added or renamed. Each item links to `/teachingintheaiera/read#chNNN`, the EPUB file name of that part.
4. Check: open the three URLs, open Chapter 1 in the reader, open the PDF tab and jump to a page.

Visitors' saved reading positions point into the old EPUB. If the chapters change a lot, bump the storage key in `read/reader.js` (`tiae-reader-v1` to `v2`, and the same key in the inline script in `read/index.html`) so everyone starts fresh instead of landing in the wrong place.

## Still to do (placeholders on the page)

- **Contact email**: footer of `teachingintheaiera/index.html`, the highlighted `[CONTACT EMAIL TO ADD]`.
- **Paperback link**: done 2026-11-09, the hero button points at the Books2Read universal link https://books2read.com/u/mdrgNO (also a `Paperback` workExample in the JSON-LD). On that date Books2Read listed the ebook only; check that the paperback appears there.

## Deep links

- `/teachingintheaiera/read#ch003` opens Chapter 1 (`ch002` is the Introduction, `ch020` Appendix C).
- `/teachingintheaiera/read#pdf-112` opens the PDF at PDF page 112 (useful in citations: "PDF p. 112").
- `/teachingintheaiera/references#ref-25` highlights reference 25.
