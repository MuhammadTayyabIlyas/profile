#!/usr/bin/env python3
"""Builds /blog/*.html, /blog/index.html, /feed.xml, /llms.txt and refreshes /sitemap.xml.

Posts live in posts.py (POSTS list). Run:  python3 docs/blog/build_blog.py
Rules (see /CLAUDE.md): UK English, no em dashes, no invented facts.
"""
import html
import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).parent))
from posts import POSTS  # noqa: E402

SITE = "https://tayyabcheema.com"
CSS_V = re.search(r'styles\.css\?v=(\d+)', (ROOT / "index.html").read_text()).group(1)
JS_V = re.search(r'script\.js\?v=(\d+)', (ROOT / "index.html").read_text()).group(1)
AUTHOR = {"@type": "Person", "name": "Muhammad Tayyab Ilyas", "url": SITE,
          "jobTitle": "Applied AI & Solutions Engineer",
          "sameAs": ["https://github.com/MuhammadTayyabIlyas"]}

NAV = """  <a class="skip-link" href="#main">Skip to content</a>

  <nav class="navbar" role="navigation" aria-label="Main navigation">
    <div class="container">
      <a href="/" class="nav-logo">Tayyab Ilyas</a>
      <button class="nav-toggle" aria-label="Toggle menu" aria-expanded="false">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5"/></svg>
      </button>
      <ul class="nav-links">
        <li><a href="/">Home</a></li>
        <li><a href="/#case-studies">Case Studies</a></li>
        <li><a href="/#projects">Projects</a></li>
        <li><a href="/blog/">Blog</a></li>
        <li><a href="/#experience">Experience</a></li>
        <li><a href="/#about">About</a></li>
        <li><a href="/#contact" class="btn btn-primary">Contact</a></li>
      </ul>
    </div>
  </nav>
"""

FOOTER = """  <footer class="footer">
    <div class="container">
      <p class="footer-copy">
        &copy; 2026 Muhammad Tayyab Ilyas &middot; Barcelona, Spain<br />
        Applied AI &amp; Solutions Engineer &middot; PhD Researcher at UAB &middot; Published MCP Server Developer
      </p>
    </div>
  </footer>
"""


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def strip_tags(s: str) -> str:
    return re.sub(r"<[^>]+>", "", s)


def head(title, desc, url, keywords, og_type, ld_blocks):
    lds = "\n".join(
        f'  <script type="application/ld+json">\n{json.dumps(b, ensure_ascii=False, indent=2)}\n  </script>'
        for b in ld_blocks)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />

  <title>{esc(title)}</title>
  <meta name="description" content="{esc(desc)}" />
  <meta name="keywords" content="{esc(keywords)}" />
  <meta name="author" content="Muhammad Tayyab Ilyas" />
  <link rel="canonical" href="{url}" />
  <link rel="alternate" type="application/rss+xml" title="Tayyab Ilyas: Engineering notes" href="{SITE}/feed.xml" />

  <meta property="og:type" content="{og_type}" />
  <meta property="og:title" content="{esc(title)}" />
  <meta property="og:description" content="{esc(desc)}" />
  <meta property="og:url" content="{url}" />
  <meta property="og:image" content="{SITE}/assets/brand/og-image.png" />
  <meta property="og:locale" content="en_GB" />

  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:site" content="@TayyabCheema" />
  <meta name="twitter:title" content="{esc(title)}" />
  <meta name="twitter:description" content="{esc(desc)}" />
  <meta name="twitter:image" content="{SITE}/assets/brand/og-image.png" />

  <link rel="icon" type="image/x-icon" href="/favicon.ico" />
  <link rel="icon" type="image/png" sizes="192x192" href="/favicon-192.png" />
  <link rel="apple-touch-icon" href="/apple-touch-icon.png" />

  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Source+Sans+3:wght@400;600;700&display=swap" rel="stylesheet" />

  <link rel="stylesheet" href="/styles.css?v={CSS_V}" />

{lds}
</head>
<body>

{NAV}"""


def post_page(p):
    url = f"{SITE}/blog/{p['slug']}.html"
    faq = p.get("faq", [])
    blocks = [
        {"@context": "https://schema.org", "@type": "BlogPosting", "headline": p["title"],
         "description": p["description"], "url": url, "mainEntityOfPage": url,
         "datePublished": p["date"], "dateModified": p.get("updated", p["date"]),
         "author": AUTHOR, "publisher": AUTHOR, "inLanguage": "en-GB",
         "image": f"{SITE}/assets/brand/og-image.png", "keywords": p["keywords"],
         "about": p.get("about", []), "wordCount": len(strip_tags(p["body"]).split())},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
            {"@type": "ListItem", "position": 2, "name": "Blog", "item": f"{SITE}/blog/"},
            {"@type": "ListItem", "position": 3, "name": p["title"], "item": url}]},
    ]
    if faq:
        blocks.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": strip_tags(a)}}
            for q, a in faq]})
    faq_html = ""
    if faq:
        items = "\n".join(f"          <h3>{esc(q)}</h3>\n          <p>{a}</p>" for q, a in faq)
        faq_html = f"""
    <section class="case-section case-alt">
      <div class="container fade-in">
        <h2 class="section-title">Questions people ask</h2>
        <div class="case-body">
{items}
        </div>
      </div>
    </section>
"""
    d = date.fromisoformat(p["date"]).strftime("%-d %B %Y")
    return head(f"{p['title']} | Tayyab Ilyas", p["description"], url, p["keywords"], "article", blocks) + f"""
  <main id="main">
    <article>
    <section class="case-hero">
      <div class="container fade-in">
        <p class="section-label"><a href="/blog/">Blog</a> &middot; {esc(p['kicker'])}</p>
        <h1 class="case-hero-title">{esc(p['title'])}</h1>
        <p class="post-meta">By <a href="/#about">Muhammad Tayyab Ilyas</a> &middot; <time datetime="{p['date']}">{d}</time> &middot; {p['minutes']} min read</p>
        <div class="answer-box">
          <div class="answer-box-label">The short answer</div>
          <p>{p['answer']}</p>
        </div>
      </div>
    </section>

    <section class="case-section">
      <div class="container fade-in">
        <div class="case-body">
{p['body']}
        </div>
      </div>
    </section>
{faq_html}
    <section class="case-section">
      <div class="container fade-in">
        <div class="case-body">
          <p><strong>About the author.</strong> Muhammad Tayyab Ilyas is an Applied AI &amp; Solutions Engineer in Barcelona who builds and operates MCP servers, multi-agent systems and the infrastructure under them. {p.get('cta_line', '')}</p>
        </div>
        <div class="case-cta">
          <a href="/#contact" class="btn btn-primary">Talk about a project</a>
          <a href="/blog/" class="btn btn-outline">More posts</a>
        </div>
      </div>
    </section>
    </article>
  </main>

{FOOTER}
  <script src="/script.js?v={JS_V}" defer></script>
</body>
</html>
"""


def index_page(posts):
    url = f"{SITE}/blog/"
    blocks = [{"@context": "https://schema.org", "@type": "Blog", "name": "Tayyab Ilyas: Engineering notes",
               "url": url, "author": AUTHOR, "inLanguage": "en-GB",
               "blogPost": [{"@type": "BlogPosting", "headline": p["title"],
                             "url": f"{SITE}/blog/{p['slug']}.html", "datePublished": p["date"]} for p in posts]}]
    items = "\n".join(f"""          <li>
            <p class="post-meta">{date.fromisoformat(p['date']).strftime('%-d %B %Y')} &middot; {esc(p['kicker'])}</p>
            <h2><a href="/blog/{p['slug']}.html">{esc(p['title'])}</a></h2>
            <p>{esc(p['description'])}</p>
          </li>""" for p in posts)
    return head("Blog: MCP servers, AI agents and the infrastructure under them | Tayyab Ilyas",
                "Engineering notes on MCP connectors, Claude, Grok and Codex agents, sandboxes and self-hosted AI infrastructure, from systems running in production.",
                url, "MCP blog, Claude connectors, AI agents, MCP server tutorial, multi-agent engineering",
                "website", blocks) + f"""
  <main id="main">
    <section class="case-hero">
      <div class="container fade-in">
        <p class="section-label">Blog</p>
        <h1 class="case-hero-title">Engineering notes</h1>
        <p class="case-hero-lede">What I learn building MCP connectors, multi-agent systems and the infrastructure under them. Every post comes from a system that runs in production, with the real problems left in.</p>
      </div>
    </section>
    <section class="case-section">
      <div class="container fade-in">
        <ul class="post-list">
{items}
        </ul>
      </div>
    </section>
  </main>

{FOOTER}
  <script src="/script.js?v={JS_V}" defer></script>
</body>
</html>
"""


def feed(posts):
    items = "\n".join(f"""    <item>
      <title>{esc(p['title'])}</title>
      <link>{SITE}/blog/{p['slug']}.html</link>
      <guid>{SITE}/blog/{p['slug']}.html</guid>
      <pubDate>{date.fromisoformat(p['date']).strftime('%a, %d %b %Y')} 09:00:00 +0000</pubDate>
      <description>{esc(p['description'])}</description>
    </item>""" for p in posts)
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>Tayyab Ilyas: Engineering notes</title>
    <link>{SITE}/blog/</link>
    <description>MCP connectors, multi-agent systems and self-hosted AI infrastructure, from systems in production.</description>
    <language>en-gb</language>
{items}
  </channel>
</rss>
"""


def llms_txt(posts):
    lines = "\n".join(f"- [{p['title']}]({SITE}/blog/{p['slug']}.html): {strip_tags(p['answer'])}" for p in posts)
    return f"""# Muhammad Tayyab Ilyas

> Applied AI & Solutions Engineer in Barcelona. Builds and operates MCP servers (Model Context Protocol connectors for Claude), multi-agent software delivery systems and self-hosted AI infrastructure. PhD researcher at Universitat Autonoma de Barcelona. Contact: tayyabcheema777@gmail.com

## Case studies

- [Claude to Grok Agent Bridge]({SITE}/projects/grok-agent-bridge.html): a remote MCP server that lets Claude watch, task and unblock a team of xAI Grok Bots on their shared cloud computer.
- [LoopCodeLab]({SITE}/projects/loopcodelab.html): multi-agent software delivery; planner, worker and reviewer agents ship one idea to web, mobile and app stores.
- [TillBridge]({SITE}/projects/tillbridge.html): an MCP server that lets grocery staff manage a catalogue by conversation and feeds a legacy Spanish TPV.
- [Paco]({SITE}/projects/paco.html): a WhatsApp voice AI assistant with live tool calls mid-call.
- [Cheema Text-to-Voice MCP Server]({SITE}/projects/cheema-tts-mcp.html): open-source local text-to-speech and voice cloning for MCP clients.

## Blog

{lines}

## Optional

- [Home and full profile]({SITE}/)
- [RSS feed]({SITE}/feed.xml)
"""


def sitemap(posts):
    text = (ROOT / "sitemap.xml").read_text()
    urls = [f"{SITE}/blog/", f"{SITE}/projects/grok-agent-bridge.html"] + [f"{SITE}/blog/{p['slug']}.html" for p in posts]
    today = max(p.get("updated", p["date"]) for p in posts)
    for u in urls:
        if f"<loc>{u}</loc>" not in text:
            text = text.replace("</urlset>", f"  <url>\n    <loc>{u}</loc>\n    <lastmod>{today}</lastmod>\n  </url>\n</urlset>")
    return text


def main():
    posts = sorted(POSTS, key=lambda p: (p["date"], p.get("order", 0)), reverse=True)
    out = ROOT / "blog"
    out.mkdir(exist_ok=True)
    for p in posts:
        assert "—" not in p["body"] + p["answer"] + p["title"], f"em dash in {p['slug']}"
        (out / f"{p['slug']}.html").write_text(post_page(p))
    (out / "index.html").write_text(index_page(posts))
    (ROOT / "feed.xml").write_text(feed(posts))
    (ROOT / "llms.txt").write_text(llms_txt(posts))
    (ROOT / "sitemap.xml").write_text(sitemap(posts))
    print(f"built {len(posts)} posts with styles v{CSS_V}")


if __name__ == "__main__":
    main()
