# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Personal brand / portfolio website for Muhammad Tayyab Ilyas (tayyabcheema.com). Positioned around one professional identity: **Applied AI & Solutions Engineer** (agentic systems, LLM integration, workflow automation, production deployment), with a supporting EdTech + PhD-research angle. Vanilla HTML/CSS/JS — no framework, no build step, no bundler, no package.json.

## Deployment & live-editing discipline

Nginx serves this directory (`/var/www/tayyabcheema.com/`) directly. **Every file edit is immediately public** at `https://tayyabcheema.com/` — there is no build, staging, or restart. Consequences to work within:

- The filesystem is the source of truth, **not** a git ref. Working on a git branch does NOT isolate the live site; edits are live the moment they're saved. Keep the site in a shippable state at all times.
- For multi-file changes, land them in a safe order: additive CSS and new subpages first, then swap `index.html` last, so no page ever references something that doesn't exist yet.
- `styles.css` and `script.js` are cache-busted with a `?v=YYYYMMDDnn` query in the `<link>`/`<script>` tags. **Bump the version on every page** when you change either file, or browsers serve stale assets.
- Nginx uses a `try_files … /index.html` fallback, so a missing path returns the homepage HTML with `200` (not `404`). Don't rely on 404s to detect broken asset links; check the file exists on disk.

**Git remote:** `https://github.com/MuhammadTayyabIlyas/profile.git` (branch `main`). Pushes authenticate via the `gh` CLI credential helper; this server has no GitHub SSH key, so do not switch the remote to SSH.

## Structure

- `index.html` — the homepage, a long single page. Section order (each an `id` used by the 8-item anchor nav): hero → value (What I do) → about → **case-studies** (4 flagship `.project-highlight` cards) → projects (`.project-card` grid) → capabilities (5 skill groups) → experience (AI track + Education track) → edtech → research (dissertation + publications) → certifications → credibility → writing → contact → footer. Carries JSON-LD (Person, ProfilePage, three SoftwareApplication, ScholarlyArticle), Open Graph and Twitter Card meta.
- `projects/*.html` — standalone case-study pages sharing one template (`.case-hero`, `.case-section`/`.case-alt`, `.case-body`, `.arch-diagram`). Deep ones: `loopcodelab.html`, `tillbridge.html`, `paco.html`, `cheema-tts-mcp.html`; plus `apkipa.html`. `tillbridge.html` additionally carries `FAQPage` + `BreadcrumbList` JSON-LD and a visible question-and-answer section, for answer-engine visibility. Each has its own JSON-LD + OG tags and must be added to `sitemap.xml`.
- `styles.css` — one file: `:root` design tokens, all component styles, animations, responsive breakpoints (640/768/1024px; the nav collapses to a hamburger below 960px).
- `script.js` — one IIFE: RAF-throttled navbar `.scrolled`, IntersectionObserver reveals (`.fade-in`→`.visible` and staggered `.reveal-item`), floating action bar, mobile nav toggle. All observers are guarded, so removing the elements they target is safe.
- `cv/` — two role-targeted CVs (`…AI-Solutions-Engineer…`, `…EdTech-AI-Product-Engineer…`). `assets/projects/` screenshots, `assets/brand/og-image.png` social card.

Section CSS class names are historical and reused across purposes — e.g. the "Projects" section (id `projects`) reuses the `.skills` container styling, and "Case Studies" reuses `.projects`. Don't assume a section's class name matches its current purpose; go by the `id`.

## Content & positioning rules (guardrails)

- **One identity.** Lead with *Applied AI & Solutions Engineer*. Do not revert the hero to a wall of competing titles ("Founder", "PhD Researcher", "Columnist" as co-equal headliners) — those are secondary context, not the headline.
- **No invented facts.** Never fabricate metrics, clients, job titles, qualifications, or capabilities. The two CVs in `/cv/` are the source of truth for experience, education, and real metrics (e.g. 127 surveys + 32 interviews, OJET publication, UAB grant, Zenodo DOI). Product metrics that aren't verified are *omitted*, never shown as visible `[Add X]` placeholders.
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
`/root/.cache/ms-playwright/chromium-1226/chrome-linux64/chrome --headless=new --no-sandbox --hide-scrollbars --ignore-certificate-errors --force-prefers-reduced-motion --window-size=W,H --screenshot=OUT URL`. Use `--force-prefers-reduced-motion` so scroll-triggered `.fade-in` content renders immediately (otherwise below-the-fold sections capture at opacity 0). The snap Chromium at `/usr/bin/chromium-browser` also works but only writes screenshots to a home-dir path (e.g. `/root/qa/`), not `/tmp`.
