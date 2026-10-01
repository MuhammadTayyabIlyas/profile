"""Blog posts. UK English, no em dashes, only verifiable facts. HTML bodies use the case-body styles."""

POSTS = [
# ---------------------------------------------------------------------------------------------------------
{
"slug": "mcp-connectors-app-store-moment",
"order": 6,
"date": "2026-10-01",
"kicker": "Opinion",
"minutes": 7,
"title": "MCP connectors are the App Store moment for AI",
"description": "Why MCP connectors for Claude and other assistants look like the 2008 App Store: a standard socket, a directory, and builders shipping capabilities into an AI that millions already use. Lessons from shipping six connectors.",
"keywords": "MCP connectors, Claude connectors, MCP app store, MCP marketplace, MCP vs API, Model Context Protocol, remote MCP server, AI agent integrations",
"about": ["Model Context Protocol", "Claude connectors", "AI app ecosystems"],
"answer": "An MCP connector is to an AI assistant what an app was to the 2008 iPhone: a standard way for anyone to add a capability to a platform people already use every day. The Model Context Protocol gives every assistant the same socket, directories now list thousands of connectors, and one builder can ship a working integration in a day. The difference is that the user of a connector is increasingly another AI, which changes what good software looks like.",
"body": """
          <h2>Why does this feel like 2008?</h2>
          <p>When the App Store opened, the phone stopped being a product and became a platform. The phone's maker no longer had to build every feature; anyone could ship one, and users installed what they needed. The Model Context Protocol does the same for AI assistants. A connector exposes a set of named tools, Claude or another client discovers them, and from then on the assistant can act in a system it was never built for.</p>
          <p>The numbers moved fast in 2026. The public MCP registry passed roughly 17,000 to 20,000 indexed servers by August, and a community index of Anthropic's own catalogue counted 3,044 Claude integrations across its web directory and in-app catalogue by late September, up from a directory of a few hundred entries in June (sources below). Search interest followed: Semrush shows US searches for &ldquo;claude connectors&rdquo; at about 1,900 a month in September 2026, roughly triple what they were three months earlier.</p>

          <h2>What exactly is an MCP connector?</h2>
          <p>A connector is a remote MCP server: a small web service that publishes tools with names, typed arguments and a description of what each does. A client such as claude.ai lists the tools, asks the user before running anything that changes data, and calls them over HTTPS with OAuth sign-in. Nothing about the AI model changes. The capability lives in the connector.</p>

          <h2>MCP or a plain API: what is the difference?</h2>
          <p>An API is written for programmers who read documentation and write client code. An MCP server is written for a model that reads tool descriptions at run time and decides which to call. That shifts the design work. A good API is complete and flexible; a good connector is narrow, explains itself in plain language and makes the dangerous operations obvious. My retail connector, TillBridge, exposes nine tools and deliberately no delete and no raw query, because the model only needs the nine.</p>

          <h2>What did shipping six connectors teach me?</h2>
          <p>In the past few months I have built and run six MCP servers: a catalogue connector for a grocery's legacy till, a gateway for coding assistants, the connector for my multi-agent platform LoopCodeLab, one that drives a Debian desktop and a Windows machine, one that creates disposable sandbox VMs, and one that lets Claude supervise a team of xAI Grok Bots. Four lessons repeated across all of them.</p>
          <ul>
            <li><strong>Distribution is solved, trust is not.</strong> Adding a connector to claude.ai takes one URL. Deciding what it may do takes most of the design: who can sign in, which tools need confirmation, what gets logged.</li>
            <li><strong>Tool annotations are product decisions.</strong> Marking a tool read-only lets the assistant run it without asking. Marking a shell read-only by mistake would let it run unconfirmed. I pin the exact read-only set in tests.</li>
            <li><strong>OAuth is where builders get stuck.</strong> Most of the support questions around custom connectors are about sign-in, not tools. I wrote up <a href="/blog/claude-connector-google-oauth-redirect-uri-mismatch.html">the redirect URI mistake that costs people hours</a>.</li>
            <li><strong>The most valuable connectors bridge things that have no API.</strong> A legacy till, a desktop, and a team of agents that can only be messaged in an app. That is where an assistant gains abilities nobody else offers.</li>
          </ul>

          <h2>Where does the analogy break?</h2>
          <p>The App Store had one gatekeeper, one payment system and one kind of user. MCP has none of those. Directories are fragmented across the official registry, vendor catalogues and community hubs, many listed servers are abandoned, and quality varies enormously. And the user is changing: when Claude supervises Grok agents through my bridge, one AI is consuming a connector on behalf of another. Software built for that reader needs smaller, sharper tools and very clear error messages, because the reader acts on them immediately.</p>

          <h2>What should a builder do now?</h2>
          <p>Pick one system your users already live in and that their assistant cannot reach. Expose the smallest set of tools that does the job, put sign-in and an audit log in from day one, and publish it where people look. The window is the same one early app developers had: the platform has users, the catalogue is still young, and a well-made niche connector stands out.</p>

          <h3>Sources</h3>
          <ul>
            <li><a href="https://github.com/rdmgator12/awesome-claude-connectors" rel="noopener">awesome-claude-connectors</a> (Claude catalogue count, September 2026)</li>
            <li><a href="https://www.dirjournal.com/blogs/claude-connectors-list" rel="noopener">Claude Connectors: the complete list</a> (directory size, June 2026)</li>
            <li><a href="https://www.agensi.io/learn/mcp-marketplace-ai-agents" rel="noopener">MCP Marketplace: why AI agents need an app store</a></li>
            <li><a href="https://truthifi.com/education/state-of-mcp-2026-ai-agents-custom-connectors" rel="noopener">MCP in 2026: which AI agents support custom connectors</a></li>
            <li>Semrush keyword data, US database, September 2026</li>
          </ul>""",
"faq": [
("What is an MCP connector?", "A remote MCP server that publishes named tools to an AI assistant such as Claude. The assistant discovers the tools, asks before running anything that changes data, and calls them over HTTPS with OAuth sign-in."),
("Is MCP replacing APIs?", "No. MCP usually sits on top of an API, a database or a command line. It repackages capabilities for a model that chooses tools at run time, so the design favours a few narrow, self-describing tools over a large flexible surface."),
("Is there an app store for MCP servers?", "Not a single one. In 2026 there is the official MCP registry, vendor catalogues such as Claude's connectors directory, and community hubs. Discovery and quality control are still the unsolved part."),
("How long does it take to build a Claude connector?", "A focused connector with a handful of tools can work in a day. Sign-in, confirmation rules, logging and failure handling are what take the time, and they matter most."),
],
"cta_line": "He has shipped six MCP connectors, from retail to multi-agent supervision.",
},
# ---------------------------------------------------------------------------------------------------------
{
"slug": "grok-bot-tasks-without-api",
"order": 5,
"date": "2026-10-01",
"kicker": "Grok Bot",
"minutes": 6,
"title": "How to give a Grok Bot tasks when there is no API",
"description": "xAI's Grok Bot has no API for sending messages. Here is a working pattern that lets Claude or any automation delegate tasks to Grok Bots through an inbox and outbox on their shared computer, with the exact standing instruction to paste.",
"keywords": "Grok Bot, Grok Bot API, xAI Grok Bot automation, delegate tasks to Grok Bot, Claude and Grok, AI agent inbox, multi-agent delegation",
"about": ["Grok Bot", "xAI", "AI agent delegation"],
"answer": "You cannot message a Grok Bot programmatically, because xAI documents no API for it; Bots are steered only from the Grok desktop and mobile apps. What you can do is use the computer the Bots share. Give each Bot an inbox, outbox and done folder, paste one standing instruction telling it to check the inbox every few minutes, and have your automation write task files there and read results from the outbox.",
"body": """
          <h2>Why is there no Grok Bot API?</h2>
          <p>Grok Bot is xAI's always-on agent product: named Bots with jobs and memory, working on a persistent cloud computer with a browser, a terminal and a file system. xAI's documentation describes talking to a Bot through the desktop and mobile apps only. The xAI API gives you the Grok models, not your Bots. If you build a Telegram bot on Grok you use the API; if you want your existing Grok Bot to do something, you message it in the app.</p>
          <p>That is fine for a person. It is a dead end for another system, and it was a dead end for me: I run eleven Bots and wanted Claude, where most of my day happens, to hand them work.</p>

          <h2>What do the Bots already share?</h2>
          <p>Their computer. On mine, every Bot has a profile, an append-only audit log of its shell commands, browser pages and tool calls, and a full conversation transcript, all as files. Across the team that was about eleven hundred logged actions. Anything a Bot can read, a Bot can be told to watch.</p>

          <h2>The inbox and outbox pattern</h2>
          <p>Each Bot gets three folders on the shared computer:</p>
<pre><code>/workspace/agent-mail/&lt;id8&gt;-&lt;name&gt;/inbox    tasks waiting
/workspace/agent-mail/&lt;id8&gt;-&lt;name&gt;/outbox   results, same file name as the task
/workspace/agent-mail/&lt;id8&gt;-&lt;name&gt;/done     tasks the Bot has finished</code></pre>
          <p>A task is a small Markdown file named by time and a random suffix, for example <code>20261001T080000Z-a1b2c3.md</code>, with a header saying who sent it and where to reply. It is written to a temporary name first and then renamed, so a Bot can never read half a task.</p>

          <h2>What do you tell the Bot?</h2>
          <p>Once, in the Grok app, paste a standing instruction with the Bot's own paths. Mine reads:</p>
<pre><code>Claude can send you tasks through files.
Every few minutes, check &lt;inbox&gt; for task files (*.md). Handle them oldest first. For each task:
1. Read it and do the work it asks for.
2. Write your result to &lt;outbox&gt;/&lt;same file name&gt;.
3. Move the task file into &lt;done&gt;.
Never delete these files. If a task is unclear, write your question as the reply
and still move the task to done. Keep doing this whenever you are running.</code></pre>

          <h2>How does Claude use it?</h2>
          <p>Through my MCP connector, Claude has three tools for this: <code>agent_mail_setup</code> returns the instruction above for a given Bot, <code>send_task</code> writes the task, and <code>agent_replies</code> reads results and lists what is still pending. Alongside them, <code>list_agents</code>, <code>agent_activity</code> and <code>agent_transcript</code> show what each Bot is doing, so Claude can check a task was picked up rather than guess. The <a href="/projects/grok-agent-bridge.html">full case study</a> covers the rest of the bridge.</p>

          <h2>What are the limits?</h2>
          <ul>
            <li><strong>It is delegation, not chat.</strong> A task waits until the Bot's next check. Minutes, not milliseconds.</li>
            <li><strong>It depends on the Bot following the instruction.</strong> Test with one Bot before rolling it out, and repeat the instruction if a Bot's memory drifts.</li>
            <li><strong>Approvals inside the Grok app still need you.</strong> If a Bot asks permission in the app, no file can answer it.</li>
          </ul>
          <p>The same pattern works for any agent that can read files and keeps running: a folder is the most portable API there is.</p>""",
"faq": [
("Does Grok Bot have an API?", "No. xAI documents no API for messaging a Grok Bot; you talk to Bots in the Grok desktop and mobile apps. The xAI API serves Grok models, not your Bots."),
("How can another AI send work to a Grok Bot?", "Through the Bots' shared computer: write a task file to a per-Bot inbox that the Bot has been instructed to check, and read the result from its outbox. Claude does this through an MCP connector."),
("How fast does a Grok Bot pick up a task this way?", "On its next inbox check, which you set in the standing instruction, typically every few minutes. It suits delegation rather than conversation."),
("Can I see what a Grok Bot is doing?", "Yes, if you can read its computer: each Bot keeps an audit log of shell commands, browser pages and tool calls, plus a conversation transcript, which a connector can summarise."),
],
"cta_line": "He built the Claude to Grok Agent Bridge described here.",
},
# ---------------------------------------------------------------------------------------------------------
{
"slug": "claude-connector-google-oauth-redirect-uri-mismatch",
"order": 4,
"date": "2026-10-01",
"kicker": "MCP tutorial",
"minutes": 7,
"title": "Claude custom connector with Google sign-in: fixing redirect_uri_mismatch",
"description": "Building a remote MCP server for claude.ai with Google OAuth and FastMCP? The redirect_uri_mismatch error almost always means the wrong callback was registered, or on the wrong Google client. The two redirect URIs explained, with working code and checks.",
"keywords": "claude custom connector, redirect_uri_mismatch, MCP server OAuth, FastMCP Google OAuth, remote MCP server, claude.ai connector Google sign-in, how to create claude mcp server",
"about": ["OAuth 2.0", "Model Context Protocol", "Claude custom connectors", "FastMCP"],
"answer": "A claude.ai custom connector with Google sign-in involves two different redirect URIs. Google must have your server's own callback, such as https://your-server/auth/callback, registered on the exact OAuth client your server uses. Claude's callback, https://claude.ai/api/mcp/auth_callback, is never registered at Google; your server allows it as a client redirect. Error 400 redirect_uri_mismatch means Google received a callback that is not on that client's list.",
"body": """
          <h2>Why are there two redirect URIs?</h2>
          <p>With FastMCP's Google provider your MCP server is an OAuth proxy. claude.ai signs in to <em>your server</em>, and your server signs in to <em>Google</em>. Each leg has its own redirect:</p>
          <table>
            <tr><th>Leg</th><th>Redirect URI</th><th>Registered where</th></tr>
            <tr><td>claude.ai to your server</td><td><code>https://claude.ai/api/mcp/auth_callback</code></td><td>Allowed by your server (code below)</td></tr>
            <tr><td>Your server to Google</td><td><code>https://your-server/auth/callback</code></td><td>Google Cloud Console, on the client your server uses</td></tr>
          </table>
          <p>Mixing them up is the most common mistake in public bug reports: people register Claude's callback at Google, then wonder why Google rejects their own.</p>

          <h2>What caused my redirect_uri_mismatch?</h2>
          <p>I hit this today on a new connector. The server log showed claude.ai reaching the consent page and the server redirecting to Google, and Google answering with the mismatch. The callback was correct; the client was not. The connector had been configured with one Google OAuth client while the redirect URI had been added to another one in the console. Pointing the server at the client that actually carried the URI fixed it in one restart. So check the client ID in your server's settings against the one you edited, character by character, before anything else.</p>

          <h2>The server side, in FastMCP</h2>
<pre><code>from fastmcp.server.auth.providers.google import GoogleProvider

CLAUDE_REDIRECT_URIS = [
    "https://claude.ai/api/mcp/auth_callback",
    "https://claude.com/api/mcp/auth_callback",
]

auth = GoogleProvider(
    client_id=env["GOOGLE_CLIENT_ID"],          # the client that carries your callback
    client_secret=env["GOOGLE_CLIENT_SECRET"],
    base_url="https://your-server",             # Google returns to base_url + /auth/callback
    required_scopes=["openid", "https://www.googleapis.com/auth/userinfo.email"],
    jwt_signing_key=env["JWT_SIGNING_KEY"],
    allowed_client_redirect_uris=CLAUDE_REDIRECT_URIS,  # only Claude may receive codes
)</code></pre>
          <p>The last line matters for security as much as for function. Without an allow-list, a phishing client could register itself through dynamic client registration and receive an authorisation code for your account. Add an email allow-list on top, so a valid Google sign-in from anyone else is still refused.</p>

          <h2>Does the reverse proxy need anything special?</h2>
          <p>Yes. The OAuth flow uses more paths than <code>/mcp</code>: <code>/authorize</code>, <code>/token</code>, <code>/register</code>, <code>/auth/callback</code>, <code>/consent</code> and the <code>/.well-known/</code> metadata. If your Nginx only forwards <code>/mcp</code>, claude.ai fails before Google is even involved. I forward the whole host to the MCP server and let it return 404 for anything it does not serve.</p>

          <h2>A checklist that finds the fault in minutes</h2>
          <ol>
            <li>Unauthenticated <code>POST /mcp</code> returns <code>401</code>. If you get 404 or 502, the proxy is wrong.</li>
            <li><code>GET /.well-known/oauth-authorization-server</code> returns <code>200</code> with your public base URL in it.</li>
            <li>The Google client in your server's settings is the one you edited in the console.</li>
            <li>That client's authorised redirect URIs contain exactly <code>https://your-server/auth/callback</code>, scheme and host included.</li>
            <li>You waited a few minutes after saving; Google applies changes with a short delay.</li>
            <li>Your server log shows <code>/authorize</code>, then <code>/consent</code>, then a 302. That proves the claude.ai side works and the fault is at Google.</li>
          </ol>""",
"faq": [
("Which redirect URI goes in Google Cloud Console for a Claude connector?", "Your own server's callback, for example https://your-server/auth/callback, on the exact OAuth client your server is configured with. Not Claude's callback."),
("Where does https://claude.ai/api/mcp/auth_callback go?", "In your MCP server's allowed client redirect URIs. It is the address claude.ai uses to receive codes from your server, so your server must accept it, but Google never sees it."),
("Why do I still get redirect_uri_mismatch after adding the URI?", "Usually because the URI was added to a different Google OAuth client from the one in your server's settings, or because the change has not propagated yet. Compare the client IDs and wait a few minutes."),
("Can I restrict a Claude connector to one Google account?", "Yes. Add an email allow-list in your MCP server's middleware and refuse every request whose verified email is not on it, even after a successful Google sign-in."),
],
"cta_line": "His connectors run behind Google sign-in with a single allowed account.",
},
# ---------------------------------------------------------------------------------------------------------
{
"slug": "three-ais-one-connector",
"order": 3,
"date": "2026-10-01",
"kicker": "Multi-agent engineering",
"minutes": 8,
"title": "Claude, Grok and Codex on one build: one plans, one writes, one reviews",
"description": "A real build where Claude designed and planned, the Grok CLI wrote the code test-first, and the Codex CLI reviewed every task. What the reviewer caught, the incident that changed my rules, and when this beats Claude Code vs Codex comparisons.",
"keywords": "Claude Code vs Codex, Grok CLI, multi-agent code review, AI code review, Claude Grok Codex workflow, AI pair programming, cross-vendor AI agents",
"about": ["Claude", "Grok CLI", "Codex CLI", "AI code review"],
"answer": "Splitting one build across three vendors worked better than asking which single tool is best. Claude wrote the design and a task-by-task plan, the Grok CLI implemented each task with tests first, and the Codex CLI reviewed every task and the whole branch. Codex caught real defects before anything shipped, including an option injection that could turn a directory listing into a delete. The price is supervision: an implementer running with auto-approve once edited files outside its task.",
"body": """
          <h2>Why use three tools instead of picking one?</h2>
          <p>&ldquo;Claude Code vs Codex&rdquo; is one of the most searched AI tooling questions this year, and the honest answer is that comparing them misses the point. Models from different vendors make different mistakes. A reviewer from another vendor does not share the writer's blind spots, which is the whole value of review. So for a recent production build, an MCP connector that lets Claude supervise a team of Grok Bots, I gave each tool one job.</p>

          <h2>Who did what?</h2>
          <table>
            <tr><th>Role</th><th>Tool</th><th>Output</th></tr>
            <tr><td>Design, plan, controller</td><td>Claude</td><td>A spec, a plan of small tasks with exact tests, a ledger of every decision</td></tr>
            <tr><td>Implementer</td><td>Grok CLI, headless</td><td>Code and tests per task, test-first, one commit each</td></tr>
            <tr><td>Reviewer</td><td>Codex CLI, read-only sandbox</td><td>Spec compliance and quality verdicts per task, a final branch review and security scan</td></tr>
          </table>
          <p>Each task went through a loop: implement, review, fix, scoped re-review, with at most five fix rounds and a fresh implementer from round four. Disagreements with the plan went to me, not to the agents.</p>

          <h2>What did the reviewer actually catch?</h2>
          <ul>
            <li><strong>A delete hiding in a list.</strong> The directory listing tool passed a path straight to <code>find</code>. A folder named <code>-delete</code> would have been read as an action. Grok checked that GNU find on the server still parses expressions after <code>--</code>, so the fix prefixes such paths with <code>./</code>.</li>
            <li><strong>A safety check with a race.</strong> The guard against talking to the wrong machine ran once per connection, and a reconnect could skip it. It now runs on every command, and fails closed if it cannot read the machine's identity.</li>
            <li><strong>Output that could lie.</strong> End-of-command markers were matched anywhere in the output, so a command could print one and fake success. Markers now carry a random token and must be the last line.</li>
            <li><strong>Silent truncation.</strong> Large listings and error output were cut without saying so; now they say so, and the important tail survives.</li>
            <li><strong>Deploy scripts that trusted the happy path.</strong> Seven issues, from disabled host-key checks to an Nginx edit that could fail half-written. All now validate, swap atomically and roll back.</li>
          </ul>
          <p>One task, the SSH layer, needed four fix rounds. Every round fixed something real, and the final version is far better than my own plan for it was.</p>

          <h2>What went wrong?</h2>
          <p>While proving that a shell snippet worked on temporary copies of two shell configuration files, the implementer's path substitution missed, and it edited the real files on the server. Its clean-up then removed a line that had been there before. I caught it by checking the files myself, and it was a one-line restore. The rule I took from it: an implementer running with auto-approve gets an explicit list of directories it may write to, and scratch work goes in a temporary directory, every time.</p>

          <h2>Was it worth it?</h2>
          <p>Yes, for anything that will run unattended. The connector shipped with 126 automated tests, several against a private SSH server, and every review finding is either fixed or recorded with a reason. For a quick feature I now build inline and review afterwards; for infrastructure, the three-vendor loop pays for itself the first time it catches a delete in a list.</p>""",
"faq": [
("Is Claude Code or Codex better?", "For production work the more useful question is how to combine them. Models from different vendors catch each other's mistakes, so using one to write and another to review finds defects a single tool misses."),
("Can the Grok CLI run headless?", "Yes. grok -p with --output-format json runs a prompt non-interactively and returns the answer, session id and cost, and --resume continues a session, which makes it usable as an implementer in a pipeline."),
("How do you stop an AI coding agent editing the wrong files?", "Give it an explicit write scope, make it use a temporary directory for experiments, run reviewers read-only, and check the files yourself after any auto-approved run."),
("What does multi-agent code review find that tests miss?", "Design-level problems: unsafe input reaching a command, checks that can be bypassed by timing, and outputs that can be spoofed. Tests prove the cases you thought of; a reviewer from another vendor brings different cases."),
],
"cta_line": "He runs multi-agent delivery in production on LoopCodeLab.",
},
# ---------------------------------------------------------------------------------------------------------
{
"slug": "claude-code-sandbox-proxmox-vms",
"order": 2,
"date": "2026-10-01",
"kicker": "AI agent sandbox",
"minutes": 7,
"title": "Disposable Proxmox VMs as a sandbox for Claude Code, Codex and Gemini",
"description": "A sandbox for AI coding agents that is a whole virtual machine: cloned from a golden image in seconds, on a walled network behind an allow-list proxy, created by Claude through an MCP connector and destroyed automatically when its time runs out.",
"keywords": "Claude Code sandbox, AI agent sandbox, sandbox for AI agents, Proxmox AI, isolated VM for coding agents, MCP sandbox, Codex sandbox, network isolation for AI agents",
"about": ["Proxmox VE", "AI agent sandboxing", "Claude Code", "Model Context Protocol"],
"answer": "The strongest sandbox for an AI coding agent is a whole virtual machine it cannot escape, on a network it cannot leave. I run these on a Proxmox host: Claude asks an MCP connector for a sandbox, the connector clones a golden image with Claude Code, Codex and Gemini preinstalled onto a walled network that reaches only allowed domains through a proxy, and a timer destroys every sandbox when its lifetime ends.",
"body": """
          <h2>Why not just use the built-in sandbox?</h2>
          <p>Container and process sandboxes are good defaults, and Claude Code's own sandbox is a sensible first layer. For untrusted repositories, though, the guidance from Anthropic and from security writers is the same: use a dedicated VM. Filesystem isolation without network isolation lets a compromised agent send your files out; network isolation without filesystem isolation lets it reach things it should not. A VM on a walled network gives you both, and it gives you a reset button.</p>

          <h2>What does the setup look like?</h2>
          <ul>
            <li><strong>A golden image.</strong> One Ubuntu 24.04 VM with Node, Claude Code, Codex and Gemini installed and the proxy configured. Never started, only cloned.</li>
            <li><strong>Linked clones.</strong> Each sandbox is a linked clone in its own Proxmox pool, so creating one takes seconds of disk work. In testing, a sandbox was ready, including its first boot configuration, in about 18 seconds.</li>
            <li><strong>A walled network.</strong> Sandboxes sit on a separate bridge whose only way out is a proxy with an allow-list of domains. The host's firewall stops them reaching each other, the owner's machines or the management network. The walls passed a 36-point test.</li>
            <li><strong>A guard.</strong> A hook refuses to start a machine that breaks the limits: at most 4 cores and 8 GB for one sandbox, and 20 GB for all of them together, so a fifth medium sandbox is refused with the reason.</li>
          </ul>

          <h2>How does Claude create one?</h2>
          <p>Through an MCP connector with seven tools: <code>create_server</code>, <code>list_servers</code>, <code>run_command</code>, <code>read_file</code>, <code>write_file</code>, <code>extend_server</code> and <code>destroy_server</code>. Creating takes a name, a size (small is 2 cores and 4 GB, medium is 4 cores and 8 GB) and a lifetime between 1 and 24 hours, four by default.</p>
          <p>The connector never reaches a sandbox over the network. It talks to the Proxmox API with a token that can only touch the sandbox pool, and runs commands through the QEMU guest agent, a virtual serial channel. A compromised sandbox therefore has no network path back to the connector, and the connector's token cannot touch any other machine on the host.</p>

          <h2>How do sandboxes die?</h2>
          <p>Every sandbox carries its owner, creation time and end of life in its own Proxmox description, so there is one source of truth and nothing to drift. A timer runs every five minutes and destroys whatever is past its end of life. Forgotten machines cannot hold memory for days, and &ldquo;start from clean&rdquo; is one call.</p>

          <h2>What about API keys?</h2>
          <p>Model keys never pass through the chat. They live in one file on the connector's machine and are copied into each new sandbox's environment at creation, readable only by root inside it. When the sandbox is destroyed, the copy goes with it.</p>

          <h2>When is this overkill?</h2>
          <p>For a trusted repository on your own laptop, the built-in sandbox is enough. A VM pays off when agents run unattended, when the code is not yours, when several customers' agents share one host, or when you want Claude in a chat on your phone to spin up a clean machine, try something, and throw it away.</p>""",
"faq": [
("What is the safest sandbox for Claude Code?", "A dedicated virtual machine on a network that can only reach allowed domains, created fresh for the task and destroyed afterwards. It isolates both the filesystem and the network."),
("Can Claude create its own sandbox VMs?", "Yes, through an MCP connector that calls the Proxmox API with a token limited to a sandbox pool. Claude asks for a size and lifetime, and the connector clones a golden image."),
("How do you stop AI agents reaching the internet freely?", "Put their machines on a separate bridge whose only route out is a proxy with an allow-list of domains, and block traffic between that bridge and every other network on the host."),
("How fast can a sandbox VM be created?", "With linked clones of a prepared golden image, in my setup about 18 seconds including first boot configuration."),
],
"cta_line": "He runs this sandbox host alongside his MCP connectors.",
},
# ---------------------------------------------------------------------------------------------------------
{
"slug": "ssh-mcp-server-reverse-tunnel",
"order": 1,
"date": "2026-10-01",
"kicker": "SSH and MCP",
"minutes": 7,
"title": "An SSH MCP server for AI agents: reverse tunnels and the three ways they break",
"description": "Giving Claude a shell on a remote machine through an SSH MCP server and a reverse tunnel. Three failure modes that cost me real time: a tunnel that loops back to itself, host keys that change on every restart, and an OpenSSH penalty that locks the connector out.",
"keywords": "SSH MCP server, reverse SSH tunnel, MCP server SSH, AI agent remote shell, PerSourcePenalties, OpenSSH lockout, ssh host key changed, ControlMaster",
"about": ["SSH", "Model Context Protocol", "OpenSSH", "AI agents"],
"answer": "An SSH MCP server lets an assistant such as Claude run commands on a remote machine, and a reverse tunnel opened by that machine means it needs no open port. It breaks in three quiet ways: the tunnel gets started on the wrong machine and loops back, the remote machine regenerates its host key on restart, and OpenSSH's PerSourcePenalties locks out a connector that probes the port. Check the remote identity on every command, keep the host key somewhere persistent, and never probe by connecting.",
"body": """
          <h2>Why a reverse tunnel?</h2>
          <p>My MCP connector runs on my own server; the machine Claude operates is a cloud computer I do not fully control. Rather than open a port on it, that machine runs <code>ssh -N -R localhost:2222:localhost:22</code> to my server. The connector then reaches it at <code>localhost:2222</code>. Nothing on the remote machine listens on the internet, and on my side the key it uses is restricted so it can hold that one tunnel and nothing else:</p>
<pre><code>restrict,port-forwarding,permitlisten="localhost:2222",command="/bin/false" ssh-ed25519 AAAA... remote</code></pre>
          <p>Every tool becomes one command over SSH with ControlMaster multiplexing, so after the first call there is no new handshake.</p>

          <h2>Failure 1: the tunnel that loops back</h2>
          <p>The tunnel script was once run on my server instead of the remote machine. Port 2222 then forwarded my server to itself. Logins worked, commands ran, and every check looked healthy, on the wrong computer. Only comparing <code>/etc/machine-id</code> at both ends showed it.</p>
          <p>The fix is a preamble on every command that reads the remote machine's id and refuses to run if it is unreadable or equals the local one. Checking once per connection is not enough; a reconnect can slip past it. The command's real exit status comes back with an end marker that carries a per-call random token, so output from the command itself can never pass for the connector's signals.</p>

          <h2>Failure 2: host keys that change on restart</h2>
          <p>The connector pins the remote host key, as it should. Then the remote machine restarted and came back with a new key. It turned out the platform resets <code>/etc</code> on every restart and keeps only the home directory, so the SSH server generated fresh keys each time. With pinning, every restart would have looked like an impostor.</p>
          <p>The fix is to keep the host key in the persistent home directory and start <code>sshd -h ~/.ssh/host_key</code> from a small keeper script, which also reopens the tunnel in a loop. A restart now changes nothing the connector can see.</p>

          <h2>Failure 3: locked out by your own health check</h2>
          <p>OpenSSH 9.8 and later include PerSourcePenalties, which penalise a source address that connects repeatedly without completing a login. A health check that opens a TCP connection to the tunnel port and closes it is exactly that. Through a reverse tunnel, every connection reaches the remote SSH server from the same local address, so a few probes would lock the connector out of the machine entirely. The implementer of my SSH layer hit this in testing; it shows up as connections being refused for no obvious reason.</p>
          <p>The fix: check that the tunnel port is listening by reading the local socket table instead of connecting. On Linux that is <code>/proc/net/tcp</code>, state <code>0A</code>.</p>

          <h2>Two settings that make tunnels self-healing</h2>
          <ul>
            <li>On the tunnel client: <code>ServerAliveInterval 30</code>, <code>ExitOnForwardFailure yes</code> and a loop that retries after ten seconds.</li>
            <li>On the server: <code>ClientAliveInterval 30</code> with <code>ClientAliveCountMax 3</code>, so a dead tunnel frees its port in about 90 seconds and the client can reclaim it.</li>
          </ul>
          <p>With those in place my connector survives restarts and network drops without anyone touching it, and when something is down its status tool says which part and the exact command that fixes it.</p>""",
"faq": [
("What is an SSH MCP server?", "An MCP server whose tools run commands and read or write files on a remote machine over SSH, so an assistant such as Claude can operate that machine through named tools with confirmation and logging."),
("Why use a reverse SSH tunnel for an AI agent?", "The remote machine opens the connection outward, so it needs no open inbound port. The connector reaches it through a local port on the server, and the tunnel key can be restricted to that single forward."),
("Why does SSH suddenly refuse connections from localhost?", "OpenSSH 9.8+ PerSourcePenalties may be penalising the address. Through a reverse tunnel every connection arrives from the same local address, so repeated connections that never log in, such as port probes, trigger it."),
("How do I stop host key warnings after a machine restarts?", "If the platform resets /etc, store the SSH host key in a persistent directory and start sshd with -h pointing at it, then pin that key on the client."),
],
"cta_line": "His SSH-based connector lets Claude supervise a team of Grok Bots.",
},
]
