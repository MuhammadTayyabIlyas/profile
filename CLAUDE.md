# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Personal brand / portfolio website for Muhammad Tayyab Ilyas (tayyabcheema.com). Positioned around one professional identity: **Applied AI & Solutions Engineer** (agentic systems, LLM integration, workflow automation, production deployment), with a supporting EdTech + PhD-research angle. Vanilla HTML/CSS/JS — no framework, no build step, no bundler, no package.json.

## Commands

There is no build step, test suite or linter for the hand-written pages. The generated parts each have a Python builder (stdlib only, run from the repo root):

```
python3 docs/publications/build_publications.py   # /publications/ page, .bib, CSL-JSON, llms.txt section
python3 docs/blog/build_blog.py                   # /blog/, feed.xml, llms.txt, sitemap additions
python3 docs/teachingintheaiera/build_book.py     # book files, unpacked EPUB, reference lists
python3 docs/indexnow.py [URL ...]                # ping Bing/IndexNow after publishing (no args = main pages)
```

Order matters when assets change: bump `?v=` in `index.html` and `projects/*.html` first, then run the publications builder, then the blog builder. Both builders read the version from `index.html`, and the blog builder rewrites `llms.txt`, pulling in `docs/publications/llms-section.md`.

nginx config: `/etc/nginx/sites-available/tayyabcheema.com.conf` (backups in `/root/tayyabcheema.com.conf.bak-*`). After editing, run `nginx -t && systemctl reload nginx`.

## Deployment & live-editing discipline

Nginx serves this directory (`/var/www/tayyabcheema.com/`) directly. **Every file edit is immediately public** at `https://tayyabcheema.com/` — there is no build, staging, or restart. Consequences to work within:

- The filesystem is the source of truth, **not** a git ref. Working on a git branch does NOT isolate the live site; edits are live the moment they're saved. Keep the site in a shippable state at all times.
- For multi-file changes, land them in a safe order: additive CSS and new subpages first, then swap `index.html` last, so no page ever references something that doesn't exist yet.
- `styles.css` and `script.js` are cache-busted with a `?v=YYYYMMDDnn` query in the `<link>`/`<script>` tags. **Bump the version on every page** when you change either file, or browsers serve stale assets.
- Site-wide, nginx uses a `try_files … /index.html` fallback, so a missing path returns the homepage HTML with `200` (not `404`). Don't rely on 404s to detect broken asset links; check the file exists on disk. Exceptions: `/teachingintheaiera/` and `/publications/` have their own location blocks and return real 404s.

**Git remote:** `https://github.com/MuhammadTayyabIlyas/profile.git` (branch `main`, **public**). Pushes authenticate via the `gh` CLI credential helper; this server has no GitHub SSH key, so do not switch the remote to SSH. Stage by explicit path, never `git add -A`: `cv/`, `docs/interview-notes/`, `docs/teachingintheaiera-src/` (the author's book sources) and `docs/teachingintheaiera/screenshots/` are deliberately untracked. `reflib/` and `subdomains/` are gitignored, so edits there are live but not versioned.

## Blog (`/blog/`, added 2026-10-01)

Posts are data, not hand-written pages: edit `docs/blog/posts.py` (one dict per post: slug, date, title, description, keywords, `answer` = the direct answer shown in the "short answer" box and used by AI answer engines, `body` HTML, `faq` pairs) and run `python3 docs/blog/build_blog.py`. It regenerates `/blog/*.html`, `/blog/index.html`, `/feed.xml` and `/llms.txt`, adds new URLs to `sitemap.xml`, and reads the current `?v=` asset versions from `index.html` (so bump versions there and in `projects/*.html` first). Each post carries BlogPosting, BreadcrumbList and FAQPage JSON-LD; the builder refuses em dashes. Keyword targets came from Semrush (US, Sept 2026); keep posts to facts from real builds.

## Book (`/teachingintheaiera`, added 2026-11-09)

*Teaching in the AI Era* (self-published, ISBN 9798237344349, DOI 10.5281/zenodo.24085773). Clean URLs: `/teachingintheaiera`, `/read` (epub.js over the unpacked EPUB in `read/book/`; online reading only, since the ebook is sold: no PDF tab, the full EPUB/PDF are never published and nginx 301s their old URLs), `/references`, and generated chapter landing pages `/teachingintheaiera/introduction` and `/chapter-1`…`13` (excerpts and reflection questions only). The teacher's workbook (PDF + Word) and citation files stay downloadable. nginx 404s everything under `/docs/`. It has its own look (navy/amber/Montserrat from the cover, `teachingintheaiera/book.css`), not the site design system. nginx has a dedicated block for these paths (exact-match locations, gzip for CSS/JS/XHTML, real 404s). Texts come verbatim from the author's files in `docs/teachingintheaiera-src/website/`; never reword them. To publish a new edition, replace the files and run `python3 docs/teachingintheaiera/build_book.py` (see `docs/teachingintheaiera/README.md`). The homepage Research section features the book above the verified publication list.

## Publications (`/publications/`) and AI visibility

Verified works live as data in `docs/publications/build_publications.py` (never add unconfirmed works). Run it, then `python3 docs/blog/build_blog.py`: it writes `/publications/index.html`, `publications.bib` (served as text/plain with CORS), CSL-JSON `publications.json`, and the Publications section that the blog builder pulls into `/llms.txt`. After publishing or changing pages, run `python3 docs/indexnow.py [URLs]` to notify Bing and other IndexNow engines (the key file sits in the web root).

## Structure

- `index.html` — the homepage, a long single page. Section order (each an `id` used by the 8-item anchor nav): hero → value (What I do) → about → **case-studies** (4 flagship `.project-highlight` cards) → projects (`.project-card` grid) → capabilities (5 skill groups) → experience (AI track + Education track) → edtech → research (featured book card + verified publication list) → certifications → credibility → writing → contact → footer. Carries JSON-LD (Person, ProfilePage, three SoftwareApplication, and a publications `@graph`: Book, ScholarlyArticle ×5, Thesis, SoftwareSourceCode), Open Graph and Twitter Card meta. The homepage publication list and its JSON-LD are hand-written, so keep them in step with `docs/publications/build_publications.py`.
- `projects/*.html` — standalone case-study pages sharing one template (`.case-hero`, `.case-section`/`.case-alt`, `.case-body`, `.arch-diagram`). Deep ones: `loopcodelab.html`, `tillbridge.html`, `paco.html`, `cheema-tts-mcp.html`, `grok-agent-bridge.html`; plus `apkipa.html`. `tillbridge.html` additionally carries `FAQPage` + `BreadcrumbList` JSON-LD and a visible question-and-answer section, for answer-engine visibility. Each has its own JSON-LD + OG tags and must be added to `sitemap.xml`.
- `styles.css` — one file: `:root` design tokens, all component styles, animations, responsive breakpoints (640/768/1024px; the nav collapses to a hamburger below 960px).
- `script.js` — one IIFE: RAF-throttled navbar `.scrolled`, IntersectionObserver reveals (`.fade-in`→`.visible` and staggered `.reveal-item`), floating action bar, mobile nav toggle. All observers are guarded, so removing the elements they target is safe.
- `cv/` (served publicly, untracked in git) — two role-targeted CVs (`…AI-Solutions-Engineer…`, `…EdTech-AI-Product-Engineer…`). `assets/projects/` screenshots, `assets/brand/og-image.png` social card.

Section CSS class names are historical and reused across purposes — e.g. the "Projects" section (id `projects`) reuses the `.skills` container styling, and "Case Studies" reuses `.projects`. Don't assume a section's class name matches its current purpose; go by the `id`.

## Content & positioning rules (guardrails)

- **One identity.** Lead with *Applied AI & Solutions Engineer*. Do not revert the hero to a wall of competing titles ("Founder", "PhD Researcher", "Columnist" as co-equal headliners) — those are secondary context, not the headline.
- **No invented facts.** Never fabricate metrics, clients, job titles, qualifications, or capabilities. The two CVs in `/cv/` are the source of truth for experience and real metrics (e.g. 127 surveys + 32 interviews, UAB grant), except that their master's degree line is wrong (it is an MSc from the University of Sargodha). Publications: the verified list in `docs/publications/build_publications.py` supersedes the CVs (the OJET paper is now published in TOJET 25(4)). Product metrics that aren't verified are *omitted*, never shown as visible `[Add X]` placeholders.
- **Don't over-claim tech.** Only list technologies evidenced by real projects. No Kubernetes / MLOps / RAG / vector DBs / distributed ML / model training. Aspirational items go under the "Next milestones" note, not the skills list.
- Primary contact is `tayyabcheema777@gmail.com` (the old `ceo@pakedx.com` was removed sitewide — don't reintroduce it). WhatsApp is a secondary channel only.
- **Prose style:** UK English spelling (colour, recognise, personalised), no em dashes, active voice.

## Design system

- **Accent:** Deep Teal `#1A6B5A`, hover `#145A4A`. A second teal set (`--teal-deep/bright/glow`) exists only for the hero ambient glow and motion accents — use the `--accent` set for everything else.
- **Backgrounds:** `--bg-primary #FAFAF8` / `--bg-secondary #F3F0EB`, alternated between sections.
- **Type:** Instrument Serif (headings, weight 400) + Source Sans 3 (body), via Google Fonts.
- **Sizing/spacing:** font sizes use `clamp()` (`--fs-xs`…`--fs-4xl`); spacing scale `--space-xs`…`--space-4xl`.

## Key patterns

- **Button links:** use the `a.btn-primary` selector (not bare `.btn-primary`) to beat the base `a { color: var(--accent) }` rule — required for white text on teal buttons.
- **Scroll reveals:** add `.fade-in` to a section's container `<div>`; JS observes and adds `.visible`. Card grids use `.reveal-item` (JS sets `--i` per sibling for a stagger). `prefers-reduced-motion` forces everything visible, so motion is enhancement-only.
- **Architecture diagrams** are hand-written inline SVG in the site palette (`#1A6B5A` on the section bg), not generated boxes. Follow the existing marker/`viewBox` style when adding one.

## Verifying changes visually

The Playwright MCP browser is often wedged. To screenshot the live site, drive Playwright's bundled Chromium directly:
`/root/.cache/ms-playwright/chromium-1254/chrome-linux64/chrome --headless=new --no-sandbox --hide-scrollbars --ignore-certificate-errors --force-prefers-reduced-motion --window-size=W,H --screenshot=OUT URL`. Use `--force-prefers-reduced-motion` so scroll-triggered `.fade-in` content renders immediately (otherwise below-the-fold sections capture at opacity 0). The build number in that path changes whenever a newer Playwright installs its browsers (it deletes the old build); if the path is missing, `ls /root/.cache/ms-playwright/`. The snap Chromium at `/usr/bin/chromium-browser` also works but only writes screenshots to a home-dir path (e.g. `/root/qa/`), not `/tmp`.
