# Portfolio Upgrade Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn tayyabcheema.com into a production-systems showcase: upgraded homepage projects section, infrastructure strip, and three case-study pages (Paco, Cheema TTS MCP, APKIPA).

**Architecture:** Vanilla HTML/CSS/JS, no build step. New case-study pages live in `/projects/` and reuse the existing `styles.css` design system, navbar, footer, and `script.js`. Screenshots live in `/assets/projects/`. The site deploys on file save (Nginx serves the working tree), so every task must leave the live site complete and consistent, and every commit is a working state.

**Tech Stack:** HTML5, CSS custom properties, vanilla JS (existing `script.js`), inline SVG diagrams, Playwright (screenshots only).

**Spec:** `docs/superpowers/specs/2026-07-01-portfolio-upgrade-design.md`

## Global Constraints

- UK English spelling (colour, recognise, personalised). No em dashes anywhere in copy. Active voice.
- Palette: accent `#1A6B5A`, hover `#145A4A`, backgrounds `#FAFAF8` / `#F3F0EB`, card `#FFFFFF`, text `#1A1A1A` / `#3A3A3A` / muted `#8A8578`, border `#E8E4DF`.
- Fonts: Instrument Serif (headings, weight 400), Source Sans 3 (body), loaded from Google Fonts exactly as on `index.html`.
- Breakpoints: 640px, 768px, 1024px. Font sizes via existing `--fs-*` clamp variables. Spacing via `--space-*`.
- Button links must use `a.btn-primary` specificity pattern (already in styles.css; do not add plain `.btn-primary` colour overrides).
- Only verifiable claims in copy. Verified facts: Paco built 2026-03-01 from 10:00 UTC to production v2 at 16:15 UTC, outbound calls at 18:52 UTC (source: `/var/www/paco-voice/JOURNEY.md`); MCP server has 5 voices, 4 languages, voice cloning, stdio/SSE/HTTP, MIT licence, listed on mcpservers.org; APKIPA pipeline runs Flutter 3.44.4, JDK 17, Android API 36, produced a signed 42MB release APK verified by apksigner, serves a TLS + basic-auth preview with an inotify auto-rebuild loop (source: `/var/www/apkipa.tayyabcheema.com/docs/superpowers/sdd-progress.md`); 17 Nginx site configs are enabled on this server. Paco's voice bridge is not running at this moment, so write "deployed to production", never "runs 24/7".
- The site is live: never leave `index.html` referencing a file that does not exist yet. Case-study pages are created (Tasks 4 to 6) before the homepage links to them (Task 7).
- Screenshots must be reviewed for private data (emails, phone numbers, tokens, call logs, terminal contents) before they land in the web root. If a capture shows anything sensitive, recapture a clean state or drop that image and its `<figure>` block.
- Commit after every task. This working tree already has uncommitted changes; Task 1 snapshots them first.

---

### Task 1: Baseline commit and repo hygiene

**Files:**
- Modify: `.gitignore`
- Commit: existing modified/untracked files (`CLAUDE.md`, `favicon.svg`, `index.html`, `script.js`, `styles.css`, `cv-tayyab-ilyas.pdf`, `robots.txt`, `sitemap.xml`)

**Interfaces:**
- Produces: a clean baseline commit so every later task's diff is only its own work. `reflib/` and `subdomains/` stay untracked by design (separate projects served from this docroot).

- [ ] **Step 1: Extend .gitignore to exclude the co-located separate projects**

Append to `.gitignore` (current content is 17 bytes; keep whatever is there and add):

```
reflib/
subdomains/
```

- [ ] **Step 2: Commit the pre-existing working-tree state as a baseline**

```bash
cd /var/www/tayyabcheema.com
git add .gitignore CLAUDE.md favicon.svg index.html script.js styles.css cv-tayyab-ilyas.pdf robots.txt sitemap.xml
git commit -m "Snapshot pre-upgrade site state (CV, robots, sitemap, pending edits)

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

- [ ] **Step 3: Verify the tree is clean apart from ignored dirs**

Run: `git status --short`
Expected: no output (docs/ plan+spec are already committed; reflib/ and subdomains/ ignored).

---

### Task 2: Visual assets

**Files:**
- Create: `assets/projects/webtmux.png`, `assets/projects/reflib.png`, `assets/projects/reelroom.png`, `assets/projects/snake-game.png`, `assets/projects/snake-signin.png`, optionally `assets/projects/paco-dashboard.png`

**Interfaces:**
- Produces: the exact filenames above; Tasks 4, 6 and 7 reference them verbatim. All images 1280x800 viewport PNGs except the two snake shots (copied as-is).

- [ ] **Step 1: Create the assets directory**

```bash
mkdir -p /var/www/tayyabcheema.com/assets/projects
```

- [ ] **Step 2: Copy the existing Snake Game store screenshots**

```bash
cp /var/www/apkipa-public/shots/iphone-6_5-2-game.png /var/www/tayyabcheema.com/assets/projects/snake-game.png
cp /var/www/apkipa-public/shots/iphone-6_5-1-signin.png /var/www/tayyabcheema.com/assets/projects/snake-signin.png
```

- [ ] **Step 3: Capture the three public-site screenshots with Playwright**

Using the Playwright browser tools, for each of these URLs:

| URL | Save as |
|---|---|
| `https://tmux.tayyabcheema.com` | `webtmux.png` |
| `https://tayyabcheema.com/reflib/` | `reflib.png` |
| `https://video.tayyabcheema.com` | `reelroom.png` |

Sequence per URL: `browser_resize` to 1280x800, `browser_navigate` to the URL, wait for load, `browser_take_screenshot` (viewport, PNG), then copy the produced file to `/var/www/tayyabcheema.com/assets/projects/<name>.png`.

- [ ] **Step 4: Optional Paco dashboard capture (bounded to two attempts)**

The dashboard is behind Nginx basic auth externally. Find its local port with `systemctl cat paco-dashboard.service | grep -iE 'port|Exec'` and `grep -riE 'listen|proxy_pass' /etc/nginx/sites-enabled/dashboard.tayyabcheema.com | head`. If a loopback port serves the UI, navigate Playwright to `http://127.0.0.1:<port>`, screenshot as above, save as `paco-dashboard.png`. If the page needs auth or renders empty after two attempts, skip this asset; Task 4 then omits its `<figure>` block.

- [ ] **Step 5: Privacy review of every captured image**

Open each PNG in `assets/projects/` with the Read tool and check for emails, phone numbers, message content, call logs, API keys, or terminal contents. In particular `webtmux.png` may show live terminal panes and `paco-dashboard.png` may show call history. If anything sensitive is visible, recapture in a clean state (e.g. tmux session list view without pane content) or delete the image and note the omission.

- [ ] **Step 6: Sanity-check sizes and commit**

Run: `ls -la /var/www/tayyabcheema.com/assets/projects/ && du -sh /var/www/tayyabcheema.com/assets/projects/`
Expected: 4 to 6 PNGs, total under 3MB (if any single PNG exceeds 800KB, recapture at 1280x800 viewport-only, not full page).

```bash
cd /var/www/tayyabcheema.com
git add assets/projects
git commit -m "Add project screenshots for portfolio showcase

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 3: CSS additions (thumbnails, infra strip, case-study pages)

**Files:**
- Modify: `styles.css` (append new component blocks after the `.fade-in` rules at line ~894, and add one rule to each existing media query)

**Interfaces:**
- Produces CSS classes consumed by Tasks 4 to 7: `.project-card-thumb`, `.projects-intro`, `.infra-strip`, `.infra-strip-title`, `.infra-strip-text`, `.infra-diagram`, `.case-hero`, `.case-hero-title`, `.case-hero-lede`, `.case-section`, `.case-alt`, `.case-body`, `.arch-diagram`, `.case-shots`, `.case-shot`, `.case-cta`.
- Consumes existing variables and classes only; no changes to existing rules.

- [ ] **Step 1: Append the new component styles**

Insert the following block into `styles.css` immediately before the `/* --- Mobile Nav Toggle --- */` comment:

```css
/* --- Project Card Thumbnails --- */
.project-card-thumb {
  width: 100%;
  aspect-ratio: 16 / 10;
  object-fit: cover;
  object-position: top;
  border-radius: var(--radius-md);
  border: 1px solid var(--border);
  margin-bottom: var(--space-md);
  background: var(--bg-secondary);
}

.projects-intro {
  font-size: var(--fs-lg);
  color: var(--text-body);
  max-width: 680px;
  margin-top: calc(-1 * var(--space-md));
  margin-bottom: var(--space-2xl);
  line-height: 1.7;
}

/* --- Infrastructure Strip --- */
.infra-strip {
  margin-top: var(--space-2xl);
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-xl);
  padding: var(--space-2xl) var(--space-xl);
  text-align: center;
}

.infra-strip-title {
  font-family: var(--font-heading);
  font-size: var(--fs-2xl);
  color: var(--text-primary);
  margin-bottom: var(--space-sm);
}

.infra-strip-text {
  font-size: var(--fs-base);
  color: var(--text-body);
  max-width: 640px;
  margin: 0 auto var(--space-xl);
  line-height: 1.75;
}

.infra-diagram {
  width: 100%;
  max-width: 760px;
  height: auto;
  margin: 0 auto;
}

/* --- Case Study Pages --- */
.case-hero {
  padding-top: calc(var(--nav-height) + var(--space-3xl));
  padding-bottom: var(--space-2xl);
}

.case-hero-title {
  font-size: var(--fs-3xl);
  max-width: 800px;
  margin-bottom: var(--space-md);
}

.case-hero-lede {
  font-size: var(--fs-lg);
  color: var(--text-body);
  max-width: 680px;
  line-height: 1.75;
  margin-top: var(--space-lg);
}

.case-section {
  padding: var(--space-2xl) 0;
}

.case-section .section-title {
  font-size: var(--fs-2xl);
  margin-bottom: var(--space-lg);
}

.case-alt {
  background-color: var(--bg-secondary);
}

.case-body {
  max-width: 680px;
}

.case-body p + p {
  margin-top: var(--space-md);
}

.case-body ul {
  padding-left: 1.25rem;
  margin-top: var(--space-md);
}

.case-body li + li {
  margin-top: var(--space-xs);
}

.arch-diagram {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: var(--space-xl);
  margin-top: var(--space-lg);
  overflow-x: auto;
}

.arch-diagram svg {
  width: 100%;
  min-width: 560px;
  height: auto;
}

.case-shots {
  display: grid;
  grid-template-columns: 1fr;
  gap: var(--space-lg);
  margin-top: var(--space-lg);
}

.case-shot {
  margin: 0;
}

.case-shot img {
  width: 100%;
  border-radius: var(--radius-md);
  border: 1px solid var(--border);
}

.case-shot figcaption {
  font-size: var(--fs-xs);
  color: var(--text-muted);
  margin-top: var(--space-xs);
}

.case-cta {
  display: flex;
  gap: var(--space-md);
  flex-wrap: wrap;
  margin-top: var(--space-xl);
}
```

- [ ] **Step 2: Add responsive rules**

Inside the existing `@media (min-width: 640px)` block, append:

```css
  .case-shots {
    grid-template-columns: 1fr 1fr;
  }
```

- [ ] **Step 3: Verify the stylesheet still parses and the live site is unaffected**

Run: `curl -s https://tayyabcheema.com/styles.css | tail -5` (confirms the file serves) and `curl -s -o /dev/null -w "%{http_code}" https://tayyabcheema.com/`
Expected: the appended CSS visible, homepage 200. Open `https://tayyabcheema.com/` with Playwright and confirm the page renders unchanged (new classes are unused so far).

- [ ] **Step 4: Commit**

```bash
cd /var/www/tayyabcheema.com
git add styles.css
git commit -m "Add CSS for card thumbnails, infra strip, and case-study pages

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 4: Case study page: Paco

**Files:**
- Create: `projects/paco.html`

**Interfaces:**
- Consumes: `.case-*` classes from Task 3, `assets/projects/paco-dashboard.png` from Task 2 (optional), existing `styles.css`, `script.js`, favicons.
- Produces: page at `https://tayyabcheema.com/projects/paco.html`, linked from the homepage in Task 7.

- [ ] **Step 1: Create `projects/paco.html` with this complete content**

If `assets/projects/paco-dashboard.png` was not captured in Task 2, omit the entire `<figure class="case-shot">...</figure>` block below and change "monitored through a custom operations dashboard, pictured below" to "monitored through a custom operations dashboard".

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />

  <title>Paco: WhatsApp Voice AI Assistant | Case Study | Tayyab Ilyas</title>
  <meta name="description" content="Case study: how I built Paco, an AI assistant that answers WhatsApp voice calls in real time with the OpenAI Realtime API, and took it from an empty folder to production in one day." />
  <meta name="author" content="Muhammad Tayyab Ilyas" />
  <link rel="canonical" href="https://tayyabcheema.com/projects/paco.html" />

  <meta property="og:type" content="article" />
  <meta property="og:title" content="Paco: WhatsApp Voice AI Assistant | Case Study" />
  <meta property="og:description" content="An AI assistant that answers WhatsApp voice calls in real time. From empty folder to production in one day." />
  <meta property="og:url" content="https://tayyabcheema.com/projects/paco.html" />
  <meta property="og:image" content="https://tayyabcheema.com/photo.png" />
  <meta property="og:locale" content="en_GB" />

  <meta name="twitter:card" content="summary" />
  <meta name="twitter:site" content="@TayyabCheema" />
  <meta name="twitter:title" content="Paco: WhatsApp Voice AI Assistant | Case Study" />
  <meta name="twitter:description" content="An AI assistant that answers WhatsApp voice calls in real time. From empty folder to production in one day." />

  <link rel="icon" type="image/x-icon" href="/favicon.ico" />
  <link rel="icon" type="image/png" sizes="192x192" href="/favicon-192.png" />
  <link rel="apple-touch-icon" href="/apple-touch-icon.png" />

  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Source+Sans+3:wght@400;600;700&display=swap" rel="stylesheet" />

  <link rel="stylesheet" href="/styles.css" />

  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "SoftwareApplication",
    "name": "Paco WhatsApp Voice AI Assistant",
    "author": { "@type": "Person", "name": "Muhammad Tayyab Ilyas" },
    "url": "https://tayyabcheema.com/projects/paco.html",
    "applicationCategory": "CommunicationApplication",
    "operatingSystem": "Linux",
    "description": "Self-hosted AI assistant that answers WhatsApp voice calls in real time using the OpenAI Realtime API, checks live data mid-call, and places outbound briefing calls."
  }
  </script>
</head>
<body>

  <nav class="navbar" role="navigation" aria-label="Main navigation">
    <div class="container">
      <a href="/" class="nav-logo">Tayyab Ilyas</a>
      <button class="nav-toggle" aria-label="Toggle menu" aria-expanded="false">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5"/></svg>
      </button>
      <ul class="nav-links">
        <li><a href="/#about">About</a></li>
        <li><a href="/#projects">Projects</a></li>
        <li><a href="/#skills">Skills</a></li>
        <li><a href="/#research">Research</a></li>
        <li><a href="mailto:ceo@pakedx.com" class="btn btn-primary">Hire Me</a></li>
      </ul>
    </div>
  </nav>

  <main>
    <section class="case-hero">
      <div class="container fade-in">
        <p class="section-label">Case Study</p>
        <h1 class="case-hero-title">Paco: a voice AI that answers WhatsApp calls</h1>
        <div class="hero-taglines">
          <span class="hero-tag">Deployed to production</span>
          <span class="hero-tag">Built in one day</span>
          <span class="hero-tag">Self-hosted</span>
        </div>
        <p class="case-hero-lede">Paco answers a normal WhatsApp voice call and holds a real-time conversation. It checks email, calendar, weather and the web while you talk, and it can call you back with a spoken briefing. I built it from an empty folder to a production deployment in a single day.</p>
      </div>
    </section>

    <section class="case-section case-alt">
      <div class="container fade-in">
        <h2 class="section-title">The problem</h2>
        <div class="case-body">
          <p>I wanted to talk to my assistant the way you talk to a person: by calling it. Not a chat window, not push-to-talk voice notes. A real WhatsApp voice call that gets answered, understood, and responded to with natural latency.</p>
          <p>WhatsApp has no public API for answering voice calls, so the interesting engineering problem was building a reliable bridge between a WhatsApp call and a real-time speech model.</p>
        </div>
      </div>
    </section>

    <section class="case-section">
      <div class="container fade-in">
        <h2 class="section-title">Architecture</h2>
        <div class="case-body">
          <p>An inbound WhatsApp call reaches the WaVoIP SDK running inside headless Chrome under Puppeteer. A Node.js bridge captures the call audio, resamples it between the 16 kHz telephony rate and the 24 kHz the model expects, and streams it to the OpenAI Realtime API over WebSocket. The model's spoken reply streams straight back to the caller.</p>
          <p>Outbound works too: a POST to the bridge's HTTP API starts a WhatsApp call to my number and delivers a spoken briefing built from live data.</p>
        </div>
        <div class="arch-diagram">
          <svg viewBox="0 0 860 200" role="img" aria-label="Paco architecture: a WhatsApp call flows through the WaVoIP SDK in headless Chrome to a Node.js bridge and the OpenAI Realtime API, and audio streams back to the caller">
            <defs>
              <marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
                <path d="M0 0L10 5L0 10z" fill="#1A6B5A"/>
              </marker>
            </defs>
            <g font-family="'Source Sans 3', system-ui, sans-serif" font-size="14" text-anchor="middle">
              <rect x="15" y="60" width="150" height="64" rx="10" fill="#FFFFFF" stroke="#1A6B5A" stroke-width="1.5"/>
              <text x="90" y="87" fill="#1A1A1A" font-weight="600">WhatsApp</text>
              <text x="90" y="107" fill="#8A8578" font-size="12">voice call</text>
              <rect x="235" y="60" width="170" height="64" rx="10" fill="#FFFFFF" stroke="#1A6B5A" stroke-width="1.5"/>
              <text x="320" y="87" fill="#1A1A1A" font-weight="600">WaVoIP SDK</text>
              <text x="320" y="107" fill="#8A8578" font-size="12">headless Chrome</text>
              <rect x="475" y="60" width="170" height="64" rx="10" fill="#FFFFFF" stroke="#1A6B5A" stroke-width="1.5"/>
              <text x="560" y="87" fill="#1A1A1A" font-weight="600">Node.js bridge</text>
              <text x="560" y="107" fill="#8A8578" font-size="12">16 kHz to 24 kHz audio</text>
              <rect x="695" y="60" width="150" height="64" rx="10" fill="#1A6B5A"/>
              <text x="770" y="87" fill="#FFFFFF" font-weight="600">OpenAI</text>
              <text x="770" y="107" fill="rgba(255,255,255,0.85)" font-size="12">Realtime API</text>
              <line x1="165" y1="92" x2="228" y2="92" stroke="#1A6B5A" stroke-width="1.5" marker-end="url(#arr)"/>
              <line x1="405" y1="92" x2="468" y2="92" stroke="#1A6B5A" stroke-width="1.5" marker-end="url(#arr)"/>
              <line x1="645" y1="92" x2="688" y2="92" stroke="#1A6B5A" stroke-width="1.5" marker-end="url(#arr)"/>
              <path d="M770 124 v40 H90 v-26" fill="none" stroke="#1A6B5A" stroke-width="1.5" stroke-dasharray="5 4" marker-end="url(#arr)"/>
              <text x="430" y="180" fill="#8A8578" font-size="12">audio response streams back to the caller</text>
            </g>
          </svg>
        </div>
      </div>
    </section>

    <section class="case-section case-alt">
      <div class="container fade-in">
        <h2 class="section-title">The build, hour by hour</h2>
        <div class="case-body">
          <p>The whole system went from nothing to production on 1 March 2026. The timeline comes straight from the project log:</p>
        </div>
        <div class="timeline" style="margin-top: var(--space-lg);">
          <div class="timeline-items">
            <div class="timeline-item">
              <span class="timeline-year">10:00</span>
              <span class="timeline-text">Research: how to bridge a WhatsApp call into a controllable audio stream</span>
            </div>
            <div class="timeline-item">
              <span class="timeline-year">14:08</span>
              <span class="timeline-text">First successful call answered by the AI</span>
            </div>
            <div class="timeline-item">
              <span class="timeline-year">16:15</span>
              <span class="timeline-text">Production v2 deployed</span>
            </div>
            <div class="timeline-item">
              <span class="timeline-year">18:26</span>
              <span class="timeline-text">Clear audio: resampling pipeline fixed for both directions</span>
            </div>
            <div class="timeline-item">
              <span class="timeline-year">18:52</span>
              <span class="timeline-text">Outbound calling live: Paco can ring me with a briefing</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="case-section">
      <div class="container fade-in">
        <h2 class="section-title">Running it for real</h2>
        <div class="case-body">
          <p>Paco runs as a daemon on my own Ubuntu server behind Nginx, deployed with PM2 and monitored through a custom operations dashboard, pictured below. Mid-call, the model calls out to tools for email, calendar, weather and web search, so answers reflect live data rather than training data.</p>
        </div>
        <div class="case-shots">
          <figure class="case-shot">
            <img src="/assets/projects/paco-dashboard.png" alt="Paco Operations Center dashboard" loading="lazy" />
            <figcaption>The Paco Operations Center, the dashboard I built to monitor calls and services.</figcaption>
          </figure>
        </div>
        <div class="project-highlight-features" style="margin-top: var(--space-xl);">
          <span class="project-feature">Node.js</span>
          <span class="project-feature">Puppeteer</span>
          <span class="project-feature">WaVoIP</span>
          <span class="project-feature">OpenAI Realtime API</span>
          <span class="project-feature">PM2</span>
          <span class="project-feature">Nginx</span>
          <span class="project-feature">Ubuntu Server</span>
        </div>
        <div class="case-cta">
          <a href="/#projects" class="btn btn-outline">Back to all projects</a>
          <a href="mailto:ceo@pakedx.com" class="btn btn-primary">Discuss a project like this</a>
        </div>
      </div>
    </section>
  </main>

  <footer class="footer">
    <div class="container">
      <p class="footer-copy">
        &copy; 2026 Muhammad Tayyab Ilyas &middot; Barcelona, Spain<br />
        AI Agent Engineer &middot; PhD Researcher @ UAB &middot; Published MCP Server Developer
      </p>
    </div>
  </footer>

  <script src="/script.js" defer></script>
</body>
</html>
```

- [ ] **Step 2: Verify the page serves and renders**

Run: `curl -s -o /dev/null -w "%{http_code}" https://tayyabcheema.com/projects/paco.html`
Expected: `200`

Open the URL with Playwright at 1280x800 and at 375x812 (mobile): headings render in Instrument Serif, diagram visible, no horizontal overflow at mobile width, nav toggle works.

- [ ] **Step 3: Commit**

```bash
cd /var/www/tayyabcheema.com
git add projects/paco.html
git commit -m "Add Paco voice assistant case study page

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 5: Case study page: Cheema Text-to-Voice MCP Server

**Files:**
- Create: `projects/cheema-tts-mcp.html`

**Interfaces:**
- Consumes: `.case-*` classes from Task 3.
- Produces: page at `https://tayyabcheema.com/projects/cheema-tts-mcp.html`, linked from the homepage in Task 7.

- [ ] **Step 1: Create `projects/cheema-tts-mcp.html` with this complete content**

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />

  <title>Cheema Text-to-Voice MCP Server | Case Study | Tayyab Ilyas</title>
  <meta name="description" content="Case study: a free, open-source MCP server that gives AI assistants local text-to-speech and voice cloning. No API keys, no cloud. Listed on mcpservers.org." />
  <meta name="author" content="Muhammad Tayyab Ilyas" />
  <link rel="canonical" href="https://tayyabcheema.com/projects/cheema-tts-mcp.html" />

  <meta property="og:type" content="article" />
  <meta property="og:title" content="Cheema Text-to-Voice MCP Server | Case Study" />
  <meta property="og:description" content="A free, open-source MCP server giving AI assistants local text-to-speech and voice cloning. No API keys, no cloud." />
  <meta property="og:url" content="https://tayyabcheema.com/projects/cheema-tts-mcp.html" />
  <meta property="og:image" content="https://tayyabcheema.com/photo.png" />
  <meta property="og:locale" content="en_GB" />

  <meta name="twitter:card" content="summary" />
  <meta name="twitter:site" content="@TayyabCheema" />
  <meta name="twitter:title" content="Cheema Text-to-Voice MCP Server | Case Study" />
  <meta name="twitter:description" content="A free, open-source MCP server giving AI assistants local text-to-speech and voice cloning." />

  <link rel="icon" type="image/x-icon" href="/favicon.ico" />
  <link rel="icon" type="image/png" sizes="192x192" href="/favicon-192.png" />
  <link rel="apple-touch-icon" href="/apple-touch-icon.png" />

  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Source+Sans+3:wght@400;600;700&display=swap" rel="stylesheet" />

  <link rel="stylesheet" href="/styles.css" />

  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "SoftwareApplication",
    "name": "Cheema Text-to-Voice MCP Server",
    "author": { "@type": "Person", "name": "Muhammad Tayyab Ilyas" },
    "url": "https://tayyabcheema.com/projects/cheema-tts-mcp.html",
    "sameAs": "https://mcpservers.org/servers/muhammadtayyabilyas/cheema-text-to-voice-mcp-server",
    "applicationCategory": "DeveloperApplication",
    "operatingSystem": "Cross-platform",
    "license": "https://opensource.org/licenses/MIT",
    "programmingLanguage": "Python",
    "description": "Free, open-source MCP server providing local text-to-speech and voice cloning to AI assistants."
  }
  </script>
</head>
<body>

  <nav class="navbar" role="navigation" aria-label="Main navigation">
    <div class="container">
      <a href="/" class="nav-logo">Tayyab Ilyas</a>
      <button class="nav-toggle" aria-label="Toggle menu" aria-expanded="false">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5"/></svg>
      </button>
      <ul class="nav-links">
        <li><a href="/#about">About</a></li>
        <li><a href="/#projects">Projects</a></li>
        <li><a href="/#skills">Skills</a></li>
        <li><a href="/#research">Research</a></li>
        <li><a href="mailto:ceo@pakedx.com" class="btn btn-primary">Hire Me</a></li>
      </ul>
    </div>
  </nav>

  <main>
    <section class="case-hero">
      <div class="container fade-in">
        <p class="section-label">Case Study</p>
        <h1 class="case-hero-title">Giving AI assistants a voice, locally</h1>
        <div class="hero-taglines">
          <span class="hero-tag">Live on mcpservers.org</span>
          <span class="hero-tag">Open source, MIT</span>
          <span class="hero-tag">No cloud required</span>
        </div>
        <p class="case-hero-lede">The Cheema Text-to-Voice MCP Server lets any MCP-capable assistant speak: five built-in voices, four languages, and voice cloning, all running on your own machine. No API keys, no cloud, no per-character billing.</p>
      </div>
    </section>

    <section class="case-section case-alt">
      <div class="container fade-in">
        <h2 class="section-title">Why build it</h2>
        <div class="case-body">
          <p>Agents increasingly need audio output: reading results aloud, voice notifications, accessibility. The existing options meant cloud TTS with API keys, cost per character, and shipping your text to a third party.</p>
          <p>The Model Context Protocol gives assistants a standard way to call tools, so I built the missing tool: a TTS server any MCP client can use, with inference running entirely locally.</p>
        </div>
      </div>
    </section>

    <section class="case-section">
      <div class="container fade-in">
        <h2 class="section-title">How it works</h2>
        <div class="case-body">
          <p>The server is written in Python and exposes speech tools over three transports, so it plugs into whatever the client supports: stdio for desktop clients, SSE and HTTP for networked ones. Speech synthesis runs on NeuTTS with espeak-ng, including cloning a voice from a short reference sample.</p>
          <ul>
            <li>Five built-in voices across four languages</li>
            <li>Voice cloning from a reference recording</li>
            <li>stdio, SSE and HTTP transports</li>
            <li>Works with Claude Desktop, Claude Code, n8n, and any MCP client</li>
            <li>MIT licensed, listed on mcpservers.org</li>
          </ul>
        </div>
        <div class="arch-diagram">
          <svg viewBox="0 0 860 150" role="img" aria-label="MCP server architecture: an MCP client connects over stdio, SSE or HTTP to the server, which synthesises speech locally with NeuTTS and espeak-ng">
            <defs>
              <marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
                <path d="M0 0L10 5L0 10z" fill="#1A6B5A"/>
              </marker>
            </defs>
            <g font-family="'Source Sans 3', system-ui, sans-serif" font-size="14" text-anchor="middle">
              <rect x="15" y="40" width="180" height="64" rx="10" fill="#FFFFFF" stroke="#1A6B5A" stroke-width="1.5"/>
              <text x="105" y="67" fill="#1A1A1A" font-weight="600">MCP client</text>
              <text x="105" y="87" fill="#8A8578" font-size="12">Claude Desktop / Code / n8n</text>
              <rect x="255" y="40" width="160" height="64" rx="10" fill="#FFFFFF" stroke="#1A6B5A" stroke-width="1.5"/>
              <text x="335" y="67" fill="#1A1A1A" font-weight="600">Transport</text>
              <text x="335" y="87" fill="#8A8578" font-size="12">stdio / SSE / HTTP</text>
              <rect x="475" y="40" width="180" height="64" rx="10" fill="#1A6B5A"/>
              <text x="565" y="67" fill="#FFFFFF" font-weight="600">MCP server</text>
              <text x="565" y="87" fill="rgba(255,255,255,0.85)" font-size="12">Python</text>
              <rect x="695" y="40" width="150" height="64" rx="10" fill="#FFFFFF" stroke="#1A6B5A" stroke-width="1.5"/>
              <text x="770" y="67" fill="#1A1A1A" font-weight="600">Local TTS</text>
              <text x="770" y="87" fill="#8A8578" font-size="12">NeuTTS + espeak-ng</text>
              <line x1="195" y1="72" x2="248" y2="72" stroke="#1A6B5A" stroke-width="1.5" marker-end="url(#arr)"/>
              <line x1="415" y1="72" x2="468" y2="72" stroke="#1A6B5A" stroke-width="1.5" marker-end="url(#arr)"/>
              <line x1="655" y1="72" x2="688" y2="72" stroke="#1A6B5A" stroke-width="1.5" marker-end="url(#arr)"/>
            </g>
          </svg>
        </div>
      </div>
    </section>

    <section class="case-section case-alt">
      <div class="container fade-in">
        <h2 class="section-title">Where it lives</h2>
        <div class="case-body">
          <p>The server is published and listed on mcpservers.org, with source on GitHub under the MIT licence. Anyone can install it and give their assistant a voice in minutes.</p>
        </div>
        <div class="case-cta">
          <a href="https://mcpservers.org/servers/muhammadtayyabilyas/cheema-text-to-voice-mcp-server" class="btn btn-primary" target="_blank" rel="noopener noreferrer">View on mcpservers.org</a>
          <a href="https://github.com/MuhammadTayyabIlyas/CHeema-Text-to-Voice-MCP-Server" class="btn btn-outline" target="_blank" rel="noopener noreferrer">GitHub</a>
          <a href="/#projects" class="btn btn-outline">Back to all projects</a>
        </div>
      </div>
    </section>
  </main>

  <footer class="footer">
    <div class="container">
      <p class="footer-copy">
        &copy; 2026 Muhammad Tayyab Ilyas &middot; Barcelona, Spain<br />
        AI Agent Engineer &middot; PhD Researcher @ UAB &middot; Published MCP Server Developer
      </p>
    </div>
  </footer>

  <script src="/script.js" defer></script>
</body>
</html>
```

- [ ] **Step 2: Verify**

Run: `curl -s -o /dev/null -w "%{http_code}" https://tayyabcheema.com/projects/cheema-tts-mcp.html`
Expected: `200`. Playwright render check at 1280x800 and 375x812 as in Task 4.

- [ ] **Step 3: Commit**

```bash
cd /var/www/tayyabcheema.com
git add projects/cheema-tts-mcp.html
git commit -m "Add MCP server case study page

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 6: Case study page: APKIPA

**Files:**
- Create: `projects/apkipa.html`

**Interfaces:**
- Consumes: `.case-*` classes from Task 3; `assets/projects/snake-game.png` and `assets/projects/snake-signin.png` from Task 2.
- Produces: page at `https://tayyabcheema.com/projects/apkipa.html`, linked from the homepage in Task 7.

- [ ] **Step 1: Create `projects/apkipa.html` with this complete content**

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />

  <title>APKIPA: Flutter Build Pipeline on a Headless Server | Case Study | Tayyab Ilyas</title>
  <meta name="description" content="Case study: a headless Ubuntu server that builds Flutter apps, serves hot-reloading web previews behind TLS, and produces signed Android release APKs." />
  <meta name="author" content="Muhammad Tayyab Ilyas" />
  <link rel="canonical" href="https://tayyabcheema.com/projects/apkipa.html" />

  <meta property="og:type" content="article" />
  <meta property="og:title" content="APKIPA: Flutter Build Pipeline on a Headless Server | Case Study" />
  <meta property="og:description" content="A headless Ubuntu server that builds Flutter apps, serves live web previews behind TLS, and produces signed Android release APKs." />
  <meta property="og:url" content="https://tayyabcheema.com/projects/apkipa.html" />
  <meta property="og:image" content="https://tayyabcheema.com/assets/projects/snake-game.png" />
  <meta property="og:locale" content="en_GB" />

  <meta name="twitter:card" content="summary" />
  <meta name="twitter:site" content="@TayyabCheema" />
  <meta name="twitter:title" content="APKIPA: Flutter Build Pipeline | Case Study" />
  <meta name="twitter:description" content="A headless Ubuntu server that builds Flutter apps, serves live web previews behind TLS, and produces signed Android release APKs." />

  <link rel="icon" type="image/x-icon" href="/favicon.ico" />
  <link rel="icon" type="image/png" sizes="192x192" href="/favicon-192.png" />
  <link rel="apple-touch-icon" href="/apple-touch-icon.png" />

  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Source+Sans+3:wght@400;600;700&display=swap" rel="stylesheet" />

  <link rel="stylesheet" href="/styles.css" />

  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "CreativeWork",
    "name": "APKIPA Flutter Build Pipeline",
    "author": { "@type": "Person", "name": "Muhammad Tayyab Ilyas" },
    "url": "https://tayyabcheema.com/projects/apkipa.html",
    "description": "A headless Ubuntu build server for Flutter apps: hot-reloading web previews behind TLS and signed Android release APKs."
  }
  </script>
</head>
<body>

  <nav class="navbar" role="navigation" aria-label="Main navigation">
    <div class="container">
      <a href="/" class="nav-logo">Tayyab Ilyas</a>
      <button class="nav-toggle" aria-label="Toggle menu" aria-expanded="false">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5"/></svg>
      </button>
      <ul class="nav-links">
        <li><a href="/#about">About</a></li>
        <li><a href="/#projects">Projects</a></li>
        <li><a href="/#skills">Skills</a></li>
        <li><a href="/#research">Research</a></li>
        <li><a href="mailto:ceo@pakedx.com" class="btn btn-primary">Hire Me</a></li>
      </ul>
    </div>
  </nav>

  <main>
    <section class="case-hero">
      <div class="container fade-in">
        <p class="section-label">Case Study</p>
        <h1 class="case-hero-title">APKIPA: a Flutter factory on a headless server</h1>
        <div class="hero-taglines">
          <span class="hero-tag">Signed release APKs</span>
          <span class="hero-tag">Live web previews</span>
          <span class="hero-tag">Headless Ubuntu</span>
        </div>
        <p class="case-hero-lede">APKIPA turns a headless Ubuntu server into a Flutter build machine: edit code, and a TLS-protected web preview rebuilds itself; run one command, and out comes a signed Android release APK. No laptop toolchain, no CI vendor.</p>
      </div>
    </section>

    <section class="case-section case-alt">
      <div class="container fade-in">
        <h2 class="section-title">The problem</h2>
        <div class="case-body">
          <p>Building mobile apps normally chains you to a workstation with the full toolchain, or to a paid CI service. I wanted the whole loop on a server I already run: write Flutter code from anywhere, see it live in a browser, and ship an installable, signed APK from the same box.</p>
        </div>
      </div>
    </section>

    <section class="case-section">
      <div class="container fade-in">
        <h2 class="section-title">What runs on the server</h2>
        <div class="case-body">
          <ul>
            <li>Flutter 3.44 with JDK 17 and the Android SDK (API 36, build-tools 36.0.0), installed and licensed on headless Ubuntu</li>
            <li>A web preview at apkipa.tayyabcheema.com behind Nginx TLS and basic auth, rebuilt automatically on save by an inotify watch loop</li>
            <li>Release signing with a managed keystore: <code>flutter build apk --release</code> produces a 42MB APK that passes apksigner verification</li>
            <li>A config toggle between the live preview and a static release build</li>
          </ul>
          <p>Getting hot reload to work behind an HTTPS reverse proxy was the hard part: Flutter's debug web server cannot initialise its debug channel through the proxy, a documented limitation. I root-caused it, switched the always-on preview to static release builds, and added the inotify auto-rebuild loop so saving a file still updates the preview.</p>
        </div>
        <div class="arch-diagram">
          <svg viewBox="0 0 860 210" role="img" aria-label="APKIPA architecture: Flutter source flows into a headless build server which produces both a TLS-protected live web preview and a signed release APK">
            <defs>
              <marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
                <path d="M0 0L10 5L0 10z" fill="#1A6B5A"/>
              </marker>
            </defs>
            <g font-family="'Source Sans 3', system-ui, sans-serif" font-size="14" text-anchor="middle">
              <rect x="15" y="75" width="160" height="64" rx="10" fill="#FFFFFF" stroke="#1A6B5A" stroke-width="1.5"/>
              <text x="95" y="102" fill="#1A1A1A" font-weight="600">Flutter source</text>
              <text x="95" y="122" fill="#8A8578" font-size="12">edit and save</text>
              <rect x="285" y="75" width="200" height="64" rx="10" fill="#1A6B5A"/>
              <text x="385" y="102" fill="#FFFFFF" font-weight="600">Headless build server</text>
              <text x="385" y="122" fill="rgba(255,255,255,0.85)" font-size="12">Flutter 3.44 &middot; JDK 17 &middot; API 36</text>
              <rect x="600" y="20" width="200" height="64" rx="10" fill="#FFFFFF" stroke="#1A6B5A" stroke-width="1.5"/>
              <text x="700" y="47" fill="#1A1A1A" font-weight="600">Live web preview</text>
              <text x="700" y="67" fill="#8A8578" font-size="12">Nginx TLS + basic auth</text>
              <rect x="600" y="130" width="200" height="64" rx="10" fill="#FFFFFF" stroke="#1A6B5A" stroke-width="1.5"/>
              <text x="700" y="157" fill="#1A1A1A" font-weight="600">Signed release APK</text>
              <text x="700" y="177" fill="#8A8578" font-size="12">apksigner verified</text>
              <line x1="175" y1="107" x2="278" y2="107" stroke="#1A6B5A" stroke-width="1.5" marker-end="url(#arr)"/>
              <text x="228" y="97" fill="#8A8578" font-size="12">inotify rebuild</text>
              <line x1="485" y1="95" x2="593" y2="58" stroke="#1A6B5A" stroke-width="1.5" marker-end="url(#arr)"/>
              <line x1="485" y1="120" x2="593" y2="156" stroke="#1A6B5A" stroke-width="1.5" marker-end="url(#arr)"/>
            </g>
          </svg>
        </div>
      </div>
    </section>

    <section class="case-section case-alt">
      <div class="container fade-in">
        <h2 class="section-title">Shipping for real: Snake Game</h2>
        <div class="case-body">
          <p>Infrastructure is only interesting if apps ship. Alongside the pipeline I built a cross-platform Snake Game in Flutter with guest play, email and Google sign-in, and a leaderboard that keeps your high score across devices, together with the store-ready support and privacy pages every published app needs.</p>
        </div>
        <div class="case-shots">
          <figure class="case-shot">
            <img src="/assets/projects/snake-game.png" alt="Snake Game gameplay on an iPhone" loading="lazy" />
            <figcaption>Gameplay: Flutter rendering the game loop on iPhone.</figcaption>
          </figure>
          <figure class="case-shot">
            <img src="/assets/projects/snake-signin.png" alt="Snake Game sign-in screen with email and Google options" loading="lazy" />
            <figcaption>Accounts: guest play, email or Google sign-in, cross-device high scores.</figcaption>
          </figure>
        </div>
        <div class="project-highlight-features" style="margin-top: var(--space-xl);">
          <span class="project-feature">Flutter</span>
          <span class="project-feature">Dart</span>
          <span class="project-feature">Android SDK</span>
          <span class="project-feature">Nginx</span>
          <span class="project-feature">Ubuntu Server</span>
          <span class="project-feature">inotify</span>
        </div>
        <div class="case-cta">
          <a href="/#projects" class="btn btn-outline">Back to all projects</a>
          <a href="mailto:ceo@pakedx.com" class="btn btn-primary">Discuss a project like this</a>
        </div>
      </div>
    </section>
  </main>

  <footer class="footer">
    <div class="container">
      <p class="footer-copy">
        &copy; 2026 Muhammad Tayyab Ilyas &middot; Barcelona, Spain<br />
        AI Agent Engineer &middot; PhD Researcher @ UAB &middot; Published MCP Server Developer
      </p>
    </div>
  </footer>

  <script src="/script.js" defer></script>
</body>
</html>
```

- [ ] **Step 2: Verify**

Run: `curl -s -o /dev/null -w "%{http_code}" https://tayyabcheema.com/projects/apkipa.html`
Expected: `200`. Playwright render check at 1280x800 and 375x812; both screenshots load (no broken images).

- [ ] **Step 3: Commit**

```bash
cd /var/www/tayyabcheema.com
git add projects/apkipa.html
git commit -m "Add APKIPA Flutter pipeline case study page

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 7: Homepage upgrade

**Files:**
- Modify: `index.html` (stats bar ~line 194-216, projects section ~line 248-297, timeline ~line 351-371)

**Interfaces:**
- Consumes: case-study pages from Tasks 4 to 6, assets from Task 2, CSS classes from Task 3.
- Produces: the upgraded live homepage.

- [ ] **Step 1: Update the stats bar**

Replace the third `stat-item` (currently `5+` / `AI/ML Projects Shipped`) with:

```html
        <div class="stat-item">
          <span class="stat-number">15+</span>
          <span class="stat-label">Self-Hosted Sites &amp; Services</span>
        </div>
```

(17 Nginx site configs are enabled on the server; 15+ is the safe claim.)

- [ ] **Step 2: Replace the entire Featured Projects section**

Replace everything from `<!-- ========== Featured Projects ========== -->` through the matching `</section>` (currently lines 248-297) with:

```html
  <!-- ========== Featured Projects ========== -->
  <section class="projects section" id="projects">
    <div class="container fade-in">
      <p class="section-label">Featured Projects</p>
      <h2 class="section-title">Live Systems &amp; Projects</h2>
      <p class="projects-intro">Most of what follows is running right now on infrastructure I operate myself. Where a demo is public, the card links straight to the live system.</p>

      <!-- Highlighted Project: Paco -->
      <div class="project-highlight">
        <div class="project-highlight-badge">Deployed to Production</div>
        <h3 class="project-highlight-title">Paco: WhatsApp Voice AI Assistant</h3>
        <p class="project-highlight-desc">An AI assistant that answers WhatsApp voice calls and holds a real-time conversation. Paco checks email, calendar, weather and the web mid-call, and places outbound briefing calls through a simple HTTP API. Built from an empty folder to production in a single day.</p>
        <div class="project-highlight-features">
          <span class="project-feature">Inbound + Outbound Calls</span>
          <span class="project-feature">OpenAI Realtime API</span>
          <span class="project-feature">Live Data Mid-Call</span>
          <span class="project-feature">Self-Hosted</span>
        </div>
        <p class="project-highlight-compat">Deployed on my own Ubuntu server behind Nginx, with a custom operations dashboard</p>
        <div class="project-highlight-tech">Node.js &middot; Puppeteer &middot; WaVoIP &middot; OpenAI Realtime API &middot; PM2</div>
        <div class="project-highlight-links">
          <a href="/projects/paco.html" class="btn btn-primary">Read the case study</a>
        </div>
      </div>

      <!-- Highlighted Project: MCP Server -->
      <div class="project-highlight">
        <div class="project-highlight-badge">Live on mcpservers.org</div>
        <h3 class="project-highlight-title">Cheema Text-to-Voice MCP Server</h3>
        <p class="project-highlight-desc">Free, open-source MCP server providing local text-to-speech and voice cloning to AI assistants. No API keys. No cloud. Runs entirely on your machine.</p>
        <div class="project-highlight-features">
          <span class="project-feature">5 Built-in Voices</span>
          <span class="project-feature">4 Languages</span>
          <span class="project-feature">Voice Cloning</span>
          <span class="project-feature">stdio/SSE/HTTP</span>
        </div>
        <p class="project-highlight-compat">Compatible with Claude Desktop, Claude Code, n8n, and any MCP client</p>
        <div class="project-highlight-tech">Python &middot; MCP Protocol &middot; NeuTTS &middot; espeak-ng &middot; MIT Licensed</div>
        <div class="project-highlight-links">
          <a href="https://mcpservers.org/servers/muhammadtayyabilyas/cheema-text-to-voice-mcp-server" class="btn btn-primary" target="_blank" rel="noopener noreferrer">View on mcpservers.org</a>
          <a href="/projects/cheema-tts-mcp.html" class="btn btn-outline">Case study</a>
          <a href="https://github.com/MuhammadTayyabIlyas/CHeema-Text-to-Voice-MCP-Server" class="btn btn-outline" target="_blank" rel="noopener noreferrer">GitHub</a>
        </div>
      </div>

      <!-- Project Grid -->
      <div class="projects-grid">
        <a href="https://tmux.tayyabcheema.com" class="project-card" target="_blank" rel="noopener noreferrer">
          <img class="project-card-thumb" src="/assets/projects/webtmux.png" alt="webtmux terminal dashboard in the browser" width="1280" height="800" loading="lazy" />
          <h3 class="project-card-name">webtmux</h3>
          <p class="project-card-desc">Self-hosted web dashboard and terminal for driving AI coding agents from a phone. xterm.js over a tmux PTY bridge, with pane previews and push notifications. Live behind this link.</p>
          <div class="project-card-tech">Node.js &middot; xterm.js &middot; tmux &middot; PWA &middot; systemd</div>
        </a>
        <a href="/projects/apkipa.html" class="project-card">
          <img class="project-card-thumb" src="/assets/projects/snake-game.png" alt="Snake Game built with Flutter running on an iPhone" width="1284" height="2778" loading="lazy" />
          <h3 class="project-card-name">APKIPA Build Pipeline</h3>
          <p class="project-card-desc">Flutter build and distribution pipeline on a headless server: hot-reloading web previews behind TLS and signed Android release APKs. Plus a shipped cross-platform game.</p>
          <div class="project-card-tech">Flutter &middot; Android SDK &middot; Nginx &middot; Ubuntu Server</div>
        </a>
        <a href="/reflib/" class="project-card" target="_blank" rel="noopener noreferrer">
          <img class="project-card-thumb" src="/assets/projects/reflib.png" alt="RefLib reference library interface" width="1280" height="800" loading="lazy" />
          <h3 class="project-card-name">RefLib</h3>
          <p class="project-card-desc">Reference manager for my PhD thesis: 590+ sources with client-side semantic search over embedded vectors and exports for citation tools. Live demo.</p>
          <div class="project-card-tech">JavaScript &middot; Embeddings &middot; Vector Search</div>
        </a>
        <a href="https://video.tayyabcheema.com" class="project-card" target="_blank" rel="noopener noreferrer">
          <img class="project-card-thumb" src="/assets/projects/reelroom.png" alt="Reel Room AI video studio" width="1280" height="800" loading="lazy" />
          <h3 class="project-card-name">Reel Room</h3>
          <p class="project-card-desc">Browser-based AI video studio, self-hosted on my own infrastructure. Live behind this link.</p>
          <div class="project-card-tech">JavaScript &middot; AI Video &middot; Nginx</div>
        </a>
        <div class="project-card">
          <h3 class="project-card-name">PakEdX WhatsApp Node for n8n</h3>
          <p class="project-card-desc">Custom n8n node connecting WhatsApp to automation workflows, running in a self-hosted Docker n8n stack alongside AI pipelines.</p>
          <div class="project-card-tech">TypeScript &middot; n8n &middot; Docker &middot; WhatsApp</div>
        </div>
        <a href="https://github.com/MuhammadTayyabIlyas/MultiLLMChat" class="project-card" target="_blank" rel="noopener noreferrer">
          <h3 class="project-card-name">MultiLLMChat</h3>
          <p class="project-card-desc">Orchestration system routing across Claude, GPT, Gemini, DeepSeek with context-aware model switching and intelligent task delegation.</p>
          <div class="project-card-tech">Python &middot; LangGraph &middot; OpenAI API &middot; Claude API &middot; Gemini API</div>
        </a>
        <a href="https://github.com/openclaw/openclaw" class="project-card" target="_blank" rel="noopener noreferrer">
          <h3 class="project-card-name">OpenClaw Contribution</h3>
          <p class="project-card-desc">Multi-LLM model orchestration architecture contribution. Agent routing logic across multiple LLM providers.</p>
          <div class="project-card-tech">Python &middot; Multi-agent systems &middot; LLM orchestration</div>
        </a>
        <div class="project-card">
          <h3 class="project-card-name">AI_Teacher</h3>
          <p class="project-card-desc">AI tool dynamically generating, managing, and grading maths problems with personalised student feedback.</p>
          <div class="project-card-tech">Python &middot; Flask &middot; scikit-learn &middot; NLTK/spaCy</div>
        </div>
        <a href="https://github.com/MuhammadTayyabIlyas/qualcoder_app" class="project-card" target="_blank" rel="noopener noreferrer">
          <h3 class="project-card-name">QualCoder App</h3>
          <p class="project-card-desc">Python desktop app for qualitative data analysis for PhD researchers.</p>
          <div class="project-card-tech">Python &middot; Pandas &middot; PyQt</div>
        </a>
      </div>

      <!-- Infrastructure Strip -->
      <div class="infra-strip">
        <h3 class="infra-strip-title">Everything here runs on infrastructure I operate</h3>
        <p class="infra-strip-text">This site and its sister services are self-hosted on an Ubuntu server I administer: Nginx terminates TLS for more than a dozen subdomains, Node services run under PM2 and systemd, and n8n runs in Docker. The portfolio is the proof.</p>
        <svg class="infra-diagram" viewBox="0 0 860 250" role="img" aria-label="Infrastructure diagram: HTTPS traffic reaches Nginx, which routes to static sites, Node services and Docker containers on one self-managed Ubuntu server">
          <defs>
            <marker id="arr2" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
              <path d="M0 0L10 5L0 10z" fill="#1A6B5A"/>
            </marker>
          </defs>
          <g font-family="'Source Sans 3', system-ui, sans-serif" font-size="14" text-anchor="middle">
            <rect x="355" y="15" width="150" height="50" rx="10" fill="#FFFFFF" stroke="#1A6B5A" stroke-width="1.5"/>
            <text x="430" y="45" fill="#1A1A1A" font-weight="600">Internet &middot; HTTPS</text>
            <rect x="330" y="100" width="200" height="60" rx="10" fill="#1A6B5A"/>
            <text x="430" y="126" fill="#FFFFFF" font-weight="600">Nginx</text>
            <text x="430" y="146" fill="rgba(255,255,255,0.85)" font-size="12">TLS via Let's Encrypt</text>
            <rect x="60" y="190" width="210" height="52" rx="10" fill="#FFFFFF" stroke="#1A6B5A" stroke-width="1.5"/>
            <text x="165" y="212" fill="#1A1A1A" font-weight="600">Static sites</text>
            <text x="165" y="230" fill="#8A8578" font-size="12">portfolio &middot; Reel Room &middot; RefLib</text>
            <rect x="325" y="190" width="210" height="52" rx="10" fill="#FFFFFF" stroke="#1A6B5A" stroke-width="1.5"/>
            <text x="430" y="212" fill="#1A1A1A" font-weight="600">Node services</text>
            <text x="430" y="230" fill="#8A8578" font-size="12">Paco &middot; webtmux &middot; dashboard</text>
            <rect x="590" y="190" width="210" height="52" rx="10" fill="#FFFFFF" stroke="#1A6B5A" stroke-width="1.5"/>
            <text x="695" y="212" fill="#1A1A1A" font-weight="600">Docker</text>
            <text x="695" y="230" fill="#8A8578" font-size="12">n8n + custom nodes</text>
            <line x1="430" y1="65" x2="430" y2="93" stroke="#1A6B5A" stroke-width="1.5" marker-end="url(#arr2)"/>
            <line x1="380" y1="160" x2="185" y2="184" stroke="#1A6B5A" stroke-width="1.5" marker-end="url(#arr2)"/>
            <line x1="430" y1="160" x2="430" y2="184" stroke="#1A6B5A" stroke-width="1.5" marker-end="url(#arr2)"/>
            <line x1="480" y1="160" x2="675" y2="184" stroke="#1A6B5A" stroke-width="1.5" marker-end="url(#arr2)"/>
          </g>
        </svg>
      </div>
    </div>
  </section>
```

If `webtmux.png`, `reflib.png` or `reelroom.png` was dropped during the Task 2 privacy review, remove that card's `<img>` line only (the card itself stays).

- [ ] **Step 3: Add a 2026 entry to the experience timeline**

Insert before the existing 2025 `timeline-item`:

```html
          <div class="timeline-item">
            <span class="timeline-year">2026</span>
            <span class="timeline-text">Production voice AI (Paco) &middot; Flutter build pipeline &middot; Self-hosted fleet of live services</span>
          </div>
```

- [ ] **Step 4: Verify the live homepage**

Run:

```bash
curl -s https://tayyabcheema.com/ | grep -oE 'class="project-card"' | wc -l
curl -s -o /dev/null -w "%{http_code}\n" https://tayyabcheema.com/projects/paco.html https://tayyabcheema.com/projects/cheema-tts-mcp.html https://tayyabcheema.com/projects/apkipa.html
```

Expected: card count 9, all three case pages 200.

Playwright: load `https://tayyabcheema.com/` at 1280x800, 768x1024 and 375x812. Confirm: two highlight cards, 9 grid cards (thumbnails render, no broken images), infra strip diagram visible, fade-in animations still fire (scroll), no horizontal overflow on mobile.

- [ ] **Step 5: Commit**

```bash
cd /var/www/tayyabcheema.com
git add index.html
git commit -m "Homepage: Live Systems showcase, Paco flagship, infra strip, 2026 timeline

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 8: SEO plumbing

**Files:**
- Modify: `sitemap.xml`, `robots.txt`, `index.html` (og:image line 19)

**Interfaces:**
- Consumes: the three case-study URLs from Tasks 4 to 6.

- [ ] **Step 1: Rewrite `sitemap.xml`**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://tayyabcheema.com/</loc>
    <lastmod>2026-07-01</lastmod>
  </url>
  <url>
    <loc>https://tayyabcheema.com/projects/paco.html</loc>
    <lastmod>2026-07-01</lastmod>
  </url>
  <url>
    <loc>https://tayyabcheema.com/projects/cheema-tts-mcp.html</loc>
    <lastmod>2026-07-01</lastmod>
  </url>
  <url>
    <loc>https://tayyabcheema.com/projects/apkipa.html</loc>
    <lastmod>2026-07-01</lastmod>
  </url>
</urlset>
```

- [ ] **Step 2: Rewrite `robots.txt`** (keeps the site open, hides internal docs)

```
User-agent: *
Allow: /
Disallow: /docs/

Sitemap: https://tayyabcheema.com/sitemap.xml
```

- [ ] **Step 3: Fix the broken og:image on the homepage**

`https://tayyabcheema.com/og-image.jpg` returns 404 (the file does not exist). In `index.html` change:

```html
  <meta property="og:image" content="https://tayyabcheema.com/og-image.jpg" />
```

to:

```html
  <meta property="og:image" content="https://tayyabcheema.com/photo.png" />
```

- [ ] **Step 4: Verify**

```bash
curl -s https://tayyabcheema.com/sitemap.xml | grep -c '<loc>'
curl -s https://tayyabcheema.com/robots.txt
curl -s -o /dev/null -w "%{http_code}" https://tayyabcheema.com/photo.png
```

Expected: 4 locs, robots shows the Disallow line, photo.png 200.

- [ ] **Step 5: Commit**

```bash
cd /var/www/tayyabcheema.com
git add sitemap.xml robots.txt index.html
git commit -m "SEO: sitemap with case studies, hide /docs, fix og:image

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 9: Full verification sweep

**Files:**
- No new files; fixes only if defects are found.

- [ ] **Step 1: Link check every href on the four pages**

```bash
cd /var/www/tayyabcheema.com
for f in index.html projects/paco.html projects/cheema-tts-mcp.html projects/apkipa.html; do
  grep -oE 'href="[^"]+"|src="[^"]+"' "$f" | sed 's/^[a-z]*="//;s/"$//' | sort -u
done | sort -u | grep -vE '^(mailto:|#|/#)' | while read -r u; do
  case "$u" in
    /*) u="https://tayyabcheema.com$u";;
  esac
  code=$(curl -s -o /dev/null -w "%{http_code}" -m 15 -L "$u")
  echo "$code $u"
done | sort
```

Expected: every line 200 (or 401 only for intentionally auth-protected demos, and 999/403 tolerated for LinkedIn/Twitter bot blocks). Fix any 404 before proceeding.

- [ ] **Step 2: Responsive and rendering pass**

With Playwright, for each of the four pages at 375x812, 768x1024 and 1280x800: no horizontal scrollbar, no broken images, headings in Instrument Serif, diagrams legible. Take one screenshot per page at 1280x800 for the final report.

- [ ] **Step 3: Structured data and content-rule check**

```bash
cd /var/www/tayyabcheema.com
for f in projects/*.html; do python3 - "$f" <<'EOF'
import json, re, sys
html = open(sys.argv[1]).read()
for m in re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S):
    json.loads(m)
print(sys.argv[1], "JSON-LD OK")
EOF
done
grep -n $'—' index.html projects/*.html || echo "no em dashes"
```

Expected: three "JSON-LD OK" lines and "no em dashes".

- [ ] **Step 4: Final commit and report**

If Steps 1 to 3 forced fixes, commit them:

```bash
cd /var/www/tayyabcheema.com
git add -A ':!reflib' ':!subdomains'
git commit -m "Verification fixes from final sweep

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

Report to the user: what changed, the four live URLs, screenshot evidence, and any dropped assets (with reasons).
