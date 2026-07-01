# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Personal brand website for Muhammad Tayyab Ilyas (tayyabcheema.com). Single-page portfolio focused on AI Agent Engineering and PhD research. Vanilla HTML/CSS/JS — no framework, no build step, no bundler.

## Deployment

Files are served directly by Nginx from `/var/www/tayyabcheema.com/`. Any file edit is immediately live at `https://tayyabcheema.com/`. No build or restart needed.

**Git remote:** `git@github.com:MuhammadTayyabIlyas/profile.git` (branch: `main`)

## Architecture

- `index.html` — Complete single-page site. Sections (in order): Navbar, Hero, About (with role cards), Featured Projects (highlighted MCP server + project grid), Skills (tech stack + timeline + languages), Research, Connect, Footer. Includes JSON-LD structured data, Open Graph, and Twitter Card meta tags.
- `styles.css` — Design system using CSS custom properties in `:root`. All component styles, animations, and responsive breakpoints (640px, 768px, 1024px) in one file.
- `script.js` — Single IIFE. Navbar scroll detection (RAF-throttled `.scrolled` class), IntersectionObserver fade-ins (`.fade-in` → `.visible`), mobile nav toggle (`.nav-links.open`).

## Design System

- **Accent:** Deep Teal `#1A6B5A`, hover `#145A4A`
- **Backgrounds:** `--bg-primary: #FAFAF8`, `--bg-secondary: #F3F0EB` (alternating sections)
- **Typography:** Instrument Serif (headings, `font-weight: 400`) + Source Sans 3 (body) via Google Fonts
- **Sizing:** All font sizes use `clamp()` for fluid scaling (`--fs-xs` through `--fs-4xl`)
- **Spacing:** `--space-xs` (0.5rem) through `--space-4xl` (6rem)

## Key Patterns

- **Button links:** Use `a.btn-primary` selector (not just `.btn-primary`) to override the base `a { color: var(--accent) }` rule. This specificity fix is required for white text on teal buttons.
- **Scroll animations:** Add `.fade-in` class to any section's container `<div>` — JS automatically observes and adds `.visible` on scroll.
- **Alternating backgrounds:** Sections alternate between `--bg-primary` and `--bg-secondary` via explicit class (`.projects`, `.connect` use secondary).
- **Project highlight:** The Cheema Text-to-Voice MCP Server has a special highlighted card with accent border, badge, and feature pills.
- **Project cards as links:** Project cards that have URLs use `<a class="project-card">` wrapping the entire card for clickable areas.

## Content Style

- UK English spelling (colour, recognise, personalised, etc.)
- No em dashes
- Active voice throughout
- Emphasis on "ideation to production" and "Published MCP Server"
