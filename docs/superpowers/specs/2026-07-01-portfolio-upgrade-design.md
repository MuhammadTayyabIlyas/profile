# Portfolio Upgrade: Live Systems Showcase + Case Studies

**Date:** 2026-07-01
**Goal:** Make tayyabcheema.com attract attention from top IT companies by surfacing the production systems already running on this server (pacoserver3). Balanced positioning: hiring portfolio, consulting credibility, and research visibility.

## Scope

Approach A: upgrade the homepage projects section and add three case-study pages. No hero redesign, no blog, no build step. Everything stays vanilla HTML/CSS/JS served by Nginx.

## 1. Homepage: "What I've Built" becomes "Live Systems & Projects"

- Two flagship highlighted cards (reuse the existing `.project-highlight` pattern):
  - **Paco** — WhatsApp voice AI assistant. Badge: "Live in production". Pills: OpenAI Realtime API, WaVoIP/Puppeteer bridge, inbound + outbound calls, live data context. Links to `/projects/paco.html`.
  - **Cheema Text-to-Voice MCP Server** — keeps its existing highlight. Badge: "Published on npm". Links to `/projects/cheema-tts-mcp.html`.
- Project grid expands to ~8 cards. Public services link live; auth-protected ones use screenshots:
  - APKIPA (shipped Android app; screenshots; links to `/projects/apkipa.html`)
  - n8n automation stack with custom nodes (screenshot or diagram)
  - reflib — vector-search reference library (live: `/reflib/`)
  - tmux web viewer (live: `tmux.tayyabcheema.com`)
  - Video tool (live: `video.tayyabcheema.com`)
  - Existing: MultiLLMChat, OpenClaw contribution, AI_Teacher (QualCoder may merge into a single "research tooling" card if the grid gets crowded)
- Impact-first one-liners on every card: what it does for a user before what it is built with.

## 2. Infrastructure strip

A short band under the grid: "This site and its sister services run on infrastructure I build and operate." Compact inline-SVG diagram: Nginx front, Docker/PM2 services, the subdomains. One sentence, one diagram, no self-congratulation.

## 3. Case-study pages

Three pages sharing one template, reusing `styles.css`, fonts, navbar, and footer from the main site:

- `/projects/paco.html` — problem, architecture diagram (WhatsApp call, WaVoIP SDK in headless Chrome, Node bridge, OpenAI Realtime API), the one-day build timeline from JOURNEY.md, stack, outcome (inbound + outbound production calls).
- `/projects/cheema-tts-mcp.html` — the published MCP server: why, design, npm listing, how agents consume it.
- `/projects/apkipa.html` — the shipped Android app: purpose, screenshots, docs/privacy/support infrastructure that shipping an app requires.

Each page: JSON-LD (`SoftwareApplication` or `CreativeWork`), Open Graph and Twitter Card tags, entry in `sitemap.xml`, `.fade-in` scroll animations, responsive at the existing breakpoints (640/768/1024px).

## 4. Visuals

- Playwright screenshots of public services (paco, reflib, tmux, video), cropped and compressed (WebP or optimised PNG) into `/assets/projects/`.
- Screenshots of auth-protected dashboard and APKIPA taken locally, scrubbed of any private data before publishing.
- Architecture diagrams as hand-written inline SVG in the site palette (Deep Teal #1A6B5A on #FAFAF8/#F3F0EB), not generic generated boxes.

## 5. Content rules

UK English, no em dashes, active voice, "ideation to production" emphasis, per CLAUDE.md. No invented metrics: only claims verifiable from the code, docs, or live services.

## 6. Error handling / verification

- Every link on the new pages must return HTTP 200 (or intentionally note auth-protected demos).
- Pages verified responsive at the three breakpoints via Playwright.
- Screenshots reviewed for leaked private data (emails, tokens, phone numbers) before going live.
- Site is production: changes land as complete, verified pages; no half-finished sections published.

## Out of scope

Hero redesign, blog/writing section, uptime badges, analytics, framework migration.
