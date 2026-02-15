# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Personal brand website for Muhammad Tayyab Ilyas (tayyabcheema.com). Single-page, newsletter-first design inspired by gregisenberg.com / sahilbloom.com / jamesclear.com. Positions Tayyab as "PhD Researcher × EdTech Founder × AI in Education Pioneer."

## Tech Stack

Vanilla HTML/CSS/JS — no framework, no build step, no bundler. Files are served directly by Nginx from `/var/www/tayyabcheema.com/`. Any change to a file is immediately live.

## File Structure

- `index.html` — Complete single-page site with 8 sections: Hero, Newsletter, About, Featured Work, Ventures, Research, Connect, Footer. Includes JSON-LD structured data, Open Graph, and Twitter Card meta tags.
- `styles.css` — Full design system using CSS custom properties. Accent color: Deep Teal `#1A6B5A`. Typography: Instrument Serif (headings) + Source Sans 3 (body) via Google Fonts. Responsive breakpoints at 640px, 768px, 1024px.
- `script.js` — IIFE with navbar scroll detection (RAF-throttled), IntersectionObserver fade-in animations, mobile nav toggle, and newsletter form handling (client-side only, no backend yet).
- `photo.png` — Profile photo (1024x1024 PNG).
- `favicon.ico`, `favicon-192.png`, `apple-touch-icon.png` — Generated from photo with circular crop on teal background.

## Design Tokens (CSS Custom Properties)

Key values defined in `:root` in `styles.css`:
- Backgrounds: `--bg-primary: #FAFAF8`, `--bg-secondary: #F3F0EB`
- Text: `--text-primary: #1A1A1A`, `--text-body: #3A3A3A`, `--text-muted: #8A8578`
- Accent: `--accent: #1A6B5A`, `--accent-hover: #145A4A`
- Typography uses `clamp()` for fluid sizing (`--fs-xs` through `--fs-4xl`)

## Deployment

No build step. Edit files in place → changes are live immediately via Nginx. Domain: `https://tayyabcheema.com/`

## Key Patterns

- Sections use `.fade-in` class for scroll-triggered animations (JS adds `.visible`)
- Navbar gets `.scrolled` class on scroll (>10px) for border/shadow appearance
- Newsletter forms are client-side only — no backend integration yet (placeholder `action="#"`)
- Mobile nav uses `.nav-toggle` button and `.nav-links.open` class toggle

## Placeholder Links

Some links still use `#` or placeholder values and need real URLs when available:
- CRIEDO Research Group profile link
- Featured Work item URLs (papers, PDFs)
- Project URLs for PakEdX, QualCoder Pro, CAITA, PrectAI venture cards
