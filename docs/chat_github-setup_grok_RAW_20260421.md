---
url: https://grok.com/c/512b163b-0688-41fa-ab23-61915fab7edb?rid=1b7fdb3c-3ccf-494b-bd7d-ad1b79d78d0e
title: "Top SKILL.md Publishing Platforms 2026 - Grok"
date: 2026-04-22T21:01:13.764Z
lang: en-US
---

Share[](/)

today (Apr 20, 2026), what are the top index sites I can publish a new SKILL.md file to and get credit

Thought for 44s

**As of April 20, 2026, the top index sites/registries for publishing a new SKILL.md-based Agent Skill (the open standard for reusable AI agent capabilities, originated by Anthropic and now cross-compatible with Claude Code, OpenAI Codex, Cursor, etc.) are the ones below.**⁠GitHub +1

These platforms give you **credit** through author attribution (usually your GitHub username), visibility in search/leaderboards, download/install tracking, versioning, and sometimes monetization or stars/feedback. Most skills are just a folder with a SKILL.md file (YAML frontmatter + instructions) plus optional scripts/references — publish the whole folder.

### 1\. ClawHub (clawhub.ai) — Largest Community Registry (Primary Recommendation for Visibility)

*   **Why top?** It's the official public skill registry for OpenClaw (and widely used across agents). It hosts tens of thousands of live skills with semantic/vector search, versioning, changelogs, and tags. High discovery for new skills.⁠Clawhub +1
*   **How to publish & get credit:** Use the clawhub CLI (clawhub skill publish ./my-skill --slug my-skill --name "My Skill"). Requires GitHub OAuth (account ≥1 week old). Your name/version shows in the registry; users can inspect, star, or comment. Free and open.
*   **Best for:** Maximum reach in the core agent ecosystem.

### 2\. skills.sh (by Vercel) — High-Visibility Open Directory & Leaderboard

*   **Why top?** Backed by Vercel with an open leaderboard, install telemetry, and CLI-first discovery. It tracks ~87k+ unique skills and shows trending/popularity. Appears in many agent tools.⁠Kdnuggets +1
*   **How to publish & get credit:** Put your skill in a public GitHub repo (recommended structure in README). No special “submit” — it indexes via installs/telemetry and shows your repo/author. Install command is npx skills add <your-github-url>.
*   **Best for:** Passive discovery + leaderboard credit once it gains traction.

### 3\. Agensi.io — Curated Marketplace (Best for Direct Credit + Monetization)

*   **Why top?** Dedicated SKILL.md marketplace with browse/download, security scans (before listing), fingerprinting for paid skills, and creator dashboards. Supports free + paid listings; agents can query it programmatically.⁠Agensi +1
*   **How to publish & get credit:** Go to agensi.io → dashboard/submit (or /skills). Upload your skill folder; it goes through automated review. You keep most revenue on paid sales (80/20 split), get full creator profile/attribution, and skills appear in agent catalogs.
*   **Best for:** Personal branding, earnings, and protected distribution.

### 4\. Skills Directory (skillsdirectory.com) — Verified/Curated Directory

*   **Why top?** Focused on high-quality, reviewed skills. All submissions are manually checked before going live. Good for serious/enterprise discoverability.[⁠Skillsdirectory](https://skillsdirectory.com/)
*   **How to publish & get credit:** Sign in with GitHub at skillsdirectory.com/submit, add your public repo or skill details. Your authorship is clearly displayed; it’s listed in categories/search.
*   **Best for:** Quality-focused exposure (less spam, more trust signal).

### 5\. SkillsMP.com (and similar large aggregators like LobeHub.com/skills) — Automatic GitHub-Based Indexing

*   **Why top?** SkillsMP is one of the biggest scrapers/aggregators (hundreds of thousands of skills indexed from GitHub). LobeHub is another high-volume one (~280k+). They pull SKILL.md files automatically.[⁠Kdnuggets](https://www.kdnuggets.com/top-5-agent-skill-marketplaces-for-building-powerful-ai-agents)
*   **How to publish & get credit:** Make your skill public on GitHub (any repo with a clear SKILL.md in a skills/ subfolder works). It gets crawled and attributed to your username. Some have explicit “Submit” flows.
*   **Best for:** Zero-effort broad reach via GitHub.

### Quick Tips to Maximize Credit & Success

*   **Start with GitHub** — Almost every aggregator crawls public repos. Use a clean repo with good README + license.
*   **Follow the spec** — Use the official Agent Skills format (agentskills.io/specification) for maximum compatibility and progressive disclosure.
*   **Security note** — Many sites auto-scan submissions. Always follow best practices (no secrets in SKILL.md).
*   **Bonus exposure** — Submit to curated awesome lists (e.g., VoltAgent/awesome-agent-skills on GitHub) via PR for extra links/credit. Some agents also surface skills from official repos like anthropics/skills.

Publish to **ClawHub + skills.sh + Agensi** first for the biggest immediate impact. Your author credit travels with the skill across agents, and popular ones get organic installs/feedback fast. Check each site’s current submission flow (they evolve quickly).

![](https://www.google.com/s2/favicons?domain=abvijaykumar.medium.com&sz=256)

![](https://www.google.com/s2/favicons?domain=mintlify.com&sz=256)

![](https://www.google.com/s2/favicons?domain=chrisreddington.com&sz=256)

365 sources

If I create multiple skills, should they each have a separate repo under github.com/jon-chun or should I combine them into a toolbox of skills under a common single repo

Thought for 25s

**For multiple skills as jon-chun, use a single "toolbox" monorepo on GitHub (e.g., jon-chun/agent-skills or jon-chun/skills-toolbox).** This is the dominant best practice in the 2026 agent skills ecosystem.⁠YouTube +1

### Why one toolbox repo (not separate repos per skill)?

*   **Ecosystem standard**: Almost every major skill collection does this — Vercel Labs (vercel-labs/agent-skills), Anthropic’s official examples, OpenClaw’s archived skills, wshobson/agents (150+ skills), and popular community toolboxes like alirezarezvani/claude-skills or JimLiu/baoyu-skills. They all use one repo with a skills/ subfolder containing each skill as its own sub-directory.⁠GitHub +1
*   **Easier maintenance & branding**: One README that showcases your entire collection, shared CI/CD, one license/roadmap, and a clean GitHub profile (instead of 10+ tiny repos cluttering github.com/jon-chun). Your author credit still appears on every skill.
*   **Indexer & installer support**:
    *   **skills.sh (Vercel)**: Natively supports it. Add a skills.json manifest at the root — one npx skills add jon-chun/agent-skills installs your whole toolbox as a bundle. Displays as a single high-visibility entry on their leaderboard.⁠GitHub +1
    *   **ClawHub**: Publish each skill individually with the CLI (clawhub skill publish ./skills/my-skill-name). The skill folder lives in your monorepo; ClawHub still attributes it to you and links back to the repo. You get separate listings + one central source of truth.[⁠Gist.github](https://gist.github.com/adhishthite/0db995ecfe2f23e09d0b2d418491982c)
    *   **Agensi.io, SkillsDirectory, LobeHub, SkillsMP**: All crawl GitHub and happily index every SKILL.md they find in subfolders. No penalty for monorepo structure.
*   **Agent compatibility**: Project-level skills (.claude/skills/, .agents/skills/, .github/skills/) and global installs all work perfectly when users clone your toolbox or install via manifest. Monorepos are explicitly supported in Claude Code, Copilot, Codex, etc.[⁠GitHub](https://github.com/shanraisshan/claude-code-best-practice/blob/main/reports/claude-skills-for-larger-mono-repos.md)
*   **Discoverability & credit**: The toolbox repo itself gets stars, forks, and visibility (“jon-chun’s Agent Skills Toolbox”), which drives more installs than scattered micro-repos. Each individual skill still gets its own name, description, version, and usage stats on the registries.

### Recommended repo structure

text

Copy

```
jon-chun/agent-skills/
├── README.md              # Overview of all your skills + install instructions
├── skills.json            # For skills.sh bundling (highly recommended)
├── skills/
│   ├── my-first-skill/    # ← each skill is its own clean folder
│   │   ├── SKILL.md
│   │   ├── scripts/
│   │   ├── references/
│   │   └── README.md (optional but nice)
│   ├── another-cool-skill/
│   │   └── SKILL.md
│   └── ...
├── .github/
│   └── workflows/         # optional CI for testing/publishing
└── LICENSE
```

### Quick start steps

1.  Create the repo jon-chun/agent-skills (or similar — keep it clear and searchable).
2.  Add the folder structure above.
3.  Write each SKILL.md following the official spec.
4.  Add a skills.json for easy skills.sh installs (see Vercel’s example format).
5.  Publish to ClawHub individually via CLI from each subfolder.
6.  Submit the repo once to skills.sh / Agensi / directories — they’ll pick up everything.

### When _would_ you want separate repos instead?

*   One skill is _massively_ popular and deserves its own stars/issues/community (rare for new creators).
*   Skills are in completely unrelated domains (e.g., one for finance, one for game dev) and you want totally independent branding.
*   You plan to hand off or monetize one skill independently.

For 95 % of creators (including most power users with 5–200 skills), the **single toolbox monorepo wins on every metric** — maintenance, discoverability, user experience, and your personal brand as jon-chun.

Start with the monorepo. You can always extract a skill into its own repo later if it explodes in popularity. This approach will get you the most credit and traction fastest across ClawHub, skills.sh, Agensi, and everywhere else. Let me know if you want a template repo or example skills.json!

![](https://www.google.com/s2/favicons?domain=datacamp.com&sz=256)

![](https://www.google.com/s2/favicons?domain=tencentcloud.com&sz=256)

![](https://www.google.com/s2/favicons?domain=medium.com&sz=256)

310 sources

  

Expert