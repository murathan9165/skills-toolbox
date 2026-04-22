# Publishing Strategy for `jon-chun/deep-thoughts`

**A Socratic Design Thinking Agent Skill**
Prepared for: Jon Chun
Date: April 20, 2026

---

## 1. Executive Summary (TL;DR)

Your supplied `SKILL_PUB_STRATEGY` document correctly identified the five most visible SKILL.md registries as of April 2026 (ClawHub, skills.sh, Agensi, skillsdirectory.com, SkillsMP/LobeHub), but it contains **three consequential errors and several critical omissions** that would waste effort and, in one case, actively damage your author reputation.

The corrected, prioritized plan is:

1. **Build the canonical GitHub repo first** (`jon-chun/deep-thoughts`) — every registry crawls GitHub; this is the single source of truth.
2. **Ship as a Claude Code *plugin marketplace***, not just a loose skill — this is Anthropic's first-party distribution channel and was **completely missing** from the supplied strategy.
3. **Register on skills.sh** (passive, telemetry-driven; run one `npx skills add` yourself to seed it).
4. **Submit to Agensi.io and skillsdirectory.com** (both do security scans; the trust signal matters for a methodology skill).
5. **Get crawled automatically** by SkillsMP and LobeHub (no action needed beyond a public repo).
6. **Wait 2–4 weeks for organic usage, then submit to VoltAgent/awesome-agent-skills** — they reject new/untested skills on purpose.
7. **Skip (or approach very cautiously) ClawHub** — the ClawHavoc supply-chain attack (Jan–Feb 2026) flooded that registry with 341–900+ malicious skills; your work will sit next to known malware, and the strategy document failed to mention this.
8. **Amplify via Simon Willison's blog, Hacker News, r/ClaudeAI, Anthropic Discord, and a launch thread on X.**

The single highest-leverage quality investment is the **`description` field** in your `SKILL.md` frontmatter. That one string — under 1024 characters — determines whether any agent ever invokes your skill. Build an eval harness before publishing.

---

## 2. Critique of the Supplied `SKILL_PUB_STRATEGY`

I verified every named registry, claim, and URL via live web search. The document is directionally right but has real problems.

### 2.1 What the document got right

The five named registries are all real and active as of April 2026. The core claims about the Agent Skills open standard, the role of `SKILL.md`, the `agentskills.io` specification site, and the GitHub-first publishing pattern are accurate. The recommendation to follow the spec for cross-agent compatibility is correct — Anthropic open-sourced the standard on December 18, 2025, and Microsoft, OpenAI, Atlassian, Figma, Cursor, and GitHub have all adopted it.

### 2.2 Errors and misleading specifics

**Error 1: Attributes skills.sh to "Vercel" without qualification.** It was launched by **Vercel Labs** (the experimental arm) on January 20, 2026, not by Vercel proper. The strategy also claims "~87k+ unique skills" tracked on skills.sh — this figure does not match verified data. The real top-line stats are install counts (e.g., `find-skills` at 579K+ installs), not a unique-skill count. Use the verified framing.

**Error 2: Overstates ClawHub's standing without mentioning its security crisis.** The document calls ClawHub the "primary recommendation for visibility" but omits the **ClawHavoc supply-chain attack**, which began January 27, 2026 and was named by Koi Security on February 1. Researchers found 341–900+ malicious skills (roughly 20% of the ecosystem at one point), many typo-squatting legitimate names, embedding Atomic Stealer (AMOS) on macOS and reverse shells on both macOS and Windows. This materially changes the calculus: publishing there now carries reputational and co-listing risk. The strategy's silence on this is its single biggest failure.

**Error 3: Inaccurate revenue-share claim for Agensi.** The document cites an "80/20 split" for paid skills on Agensi.io. That specific figure is not substantiated in current public documentation. Treat monetization terms as "check the dashboard" rather than a quoted number.

**Minor imprecisions.** "OpenClaw has 220k stars" appears in one promotional blog but is not a primary source. "LobeHub ~280k+" and "SkillsMP hundreds of thousands" are roughly in the right ballpark (SkillsMP advertises 800K+ aggregated skills; LobeHub is smaller and more curated), but the strategy conflates aggregator index size with real active-skill counts.

### 2.3 Critical omissions

**Omission 1 (the big one): Claude Code plugin marketplaces.** This is Anthropic's **official, first-party** distribution channel for Claude users. You publish a plugin marketplace as a Git repo; users install with `claude plugin marketplace add jon-chun/deep-thoughts` and then `claude plugin install <name>@deep-thoughts`. There is also an `anthropics/claude-plugins-official` directory for curated submissions. A Socratic-thinking skill aimed at Claude-native users *belongs here first*. The supplied strategy never mentions it.

**Omission 2: `description` field engineering.** The spec caps descriptions at 1,024 characters. That field is the *sole* trigger signal for every downstream agent. Anthropic's own guidance explicitly warns that Claude tends to **under-trigger** skills, and recommends writing descriptions that are slightly "pushy," in third person, with both "what it does" and "when to use it" concrete triggers. Skipping this means your skill ships but never fires.

**Omission 3: Eval harness.** Best practice is 20 trigger tests (mix of should-trigger and should-not-trigger) saved as JSON, run against candidate description variants. No sophisticated publishing plan survives a skill that doesn't fire.

**Omission 4: Cross-agent reach beyond Claude.** Codex (OpenAI), Cursor, VS Code Copilot, Gemini CLI, OpenCode, Windsurf, and Microsoft Agent Framework all consume the same SKILL.md format. Your deep-thoughts skill works in all of them without modification. The strategy treats this as a vague bonus; it should be central.

**Omission 5: Awesome-list gating.** `VoltAgent/awesome-agent-skills` — the highest-signal curated list — explicitly rejects skills that are brand new. Their `CONTRIBUTING.md` literally says "skills created 3 hours ago are not submitted" and prioritizes community-adopted work. Submitting too early burns the shot.

**Omission 6: Announcement surface.** Skill adoption is driven as much by Simon Willison's weblog, Hacker News "Show HN" posts, and the Anthropic Discord / r/ClaudeAI subreddit as by registry listings. These are free distribution and ignored in the strategy.

**Omission 7: Positioning for a methodology skill.** Every registry leaderboard is dominated by coding utilities (`find-skills`, `react-best-practices`, `web-design-guidelines`). A Socratic design-thinking skill competes in a different lane — the good news is there's less noise; the bad news is that keyword-matching descriptions tuned for engineering will under-surface it. You need description terms a product designer, researcher, or strategist would actually type.

---

## 3. Pre-Publish Checklist (do this *before* any submission)

These gates matter more than where you publish. A well-built skill on only two registries will out-perform a sloppy skill on all five.

### 3.1 Repository structure

Your canonical repo should look like this, rooted at `github.com/jon-chun/deep-thoughts`:

```
deep-thoughts/
├── SKILL.md                   # Required: YAML frontmatter + instructions
├── README.md                  # For humans browsing GitHub
├── LICENSE                    # MIT or Apache-2.0 recommended
├── CHANGELOG.md               # Semver history
├── .claude-plugin/
│   └── plugin.json            # For Claude Code plugin marketplace
├── marketplace.json           # If you want the repo itself to be a marketplace
├── scripts/                   # Optional: executable helpers
├── references/                # Optional: docs loaded on demand
├── assets/                    # Optional: templates, prompts
└── evals/
    └── trigger-tests.json     # 20 should/shouldn't-trigger cases
```

Keep it single-skill for now. Adding siblings later is easy; starting with sprawl isn't.

### 3.2 `SKILL.md` frontmatter (the 1,024-character fight)

Minimum required fields are `name` and `description`. Write the description in **third person**, include the *what* and the *when*, and seed it with terms your actual users will type. For a Socratic design-thinking skill, candidate trigger terms include: `socratic questioning`, `design thinking`, `first-principles`, `assumption surfacing`, `problem framing`, `root-cause`, `critique`, `devil's advocate`, `steelman`, `premortem`, `five whys`, `reframe`, `pre-mortem analysis`, `decision quality`.

Draft example (tune against your evals):

```yaml
---
name: deep-thoughts
description: "Guides the agent through Socratic, design-thinking-style reasoning before answering or
 deciding. Use this whenever the user asks for help thinking through a problem, framing a decision,
 challenging an assumption, running a premortem, steelmanning an argument, surfacing hidden
 constraints, asking 'five whys', doing root-cause analysis, or otherwise wants rigorous
 first-principles deliberation rather than a direct answer. Especially useful for strategy,
 product decisions, research design, ethical tradeoffs, and ambiguous open-ended prompts where
 jumping to a solution would skip important questions."
version: 0.1.0
author: jon-chun
license: MIT
---
```

Stay under 1,024 chars. No XML tags inside the description. The description is what gets injected into every downstream agent's system prompt — treat it like ad copy for LLMs.

### 3.3 Build a trigger-eval harness

Before publishing, save `evals/trigger-tests.json`:

```json
[
  {"query": "Help me think through whether we should pivot our research direction", "should_trigger": true},
  {"query": "What questions should I ask before deciding?", "should_trigger": true},
  {"query": "Steelman the opposing view on X", "should_trigger": true},
  {"query": "Run a premortem on this launch", "should_trigger": true},
  {"query": "What's the capital of France?", "should_trigger": false},
  {"query": "Write a Python function that reverses a string", "should_trigger": false}
  ...
]
```

Target 20 cases, 60/40 should/shouldn't. Iterate the description against them. Anthropic's own `skill-creator` skill (in `anthropics/skills`) automates this — worth using.

### 3.4 Repo hygiene that boosts discovery

Set GitHub **topics** including `claude-skill`, `agent-skill`, `skill-md`, `socratic`, `design-thinking`, `reasoning`. Add an OG preview image (social cards matter on X/Mastodon). Enable Discussions. Write a README that includes: one-sentence pitch, an animated demo or transcript snippet, install commands for Claude Code / Codex / Cursor, and a link to the spec. Tag a clean `v0.1.0` release with a CHANGELOG entry.

---

## 4. Tiered Publishing Plan (by ROI)

### Tier 1 — Foundation (mandatory, day 0)

**Publish the GitHub repo publicly.** Everything else depends on this. License it explicitly (MIT or Apache-2.0). Tag the first release as `v0.1.0`. Make sure `SKILL.md` is at the path any crawler expects — either at the repo root, or inside a `skills/deep-thoughts/` subfolder if you plan to host multiple.

### Tier 2 — First-party Claude channel (highest-value, ~1 hour)

**Ship as a Claude Code plugin marketplace.** Add a `.claude-plugin/plugin.json` describing the plugin and a top-level `marketplace.json` listing it. Users install with a single command:

```bash
claude plugin marketplace add jon-chun/deep-thoughts
claude plugin install deep-thoughts@deep-thoughts
```

See `code.claude.com/docs/en/plugin-marketplaces` for the exact manifest schema. This is the path Anthropic recommends and the most reliable way to be installed *inside* Claude Code where methodology skills are most valuable.

After the plugin is stable and actually used, **open a submission/issue to `anthropics/claude-plugins-official`**. That directory curates high-quality plugins and is Anthropic-managed — inclusion is a major credibility and reach signal. Don't submit on day 1.

### Tier 3 — Passive-telemetry registry (~10 minutes)

**Register on skills.sh.** There is no submission form; it is driven entirely by install telemetry from the `npx skills add` CLI. To seed:

```bash
npx skills add jon-chun/deep-thoughts
```

Do this yourself from a clean machine (anonymous, aggregate only). Ask two or three colleagues to do the same so the skill appears on the leaderboard with nonzero installs. Once organic adoption starts, position on the leaderboard compounds.

### Tier 4 — Curated security-scanned marketplaces (~30 minutes each)

**Submit to Agensi.io.** Go to `agensi.io/submit` (or the dashboard), upload your skill folder (or link the repo), let the automated security scan run. Free listings are available alongside paid. You get a creator profile with attribution. The security scan badge is a real trust signal for enterprise-adjacent users.

**Submit to skillsdirectory.com.** Sign in with GitHub at `skillsdirectory.com/submit` and add the public repo. Every submission is manually reviewed — expect days, not hours — but the curation is the point. Less spam, better co-listing.

### Tier 5 — Auto-indexing aggregators (zero effort)

**SkillsMP.com and LobeHub.com/skills** crawl public GitHub repos that follow the `SKILL.md` convention. If your repo is public with the correct structure, you will be indexed automatically within days to weeks. No submission needed. Attribution flows from your GitHub username. After it appears, you can request category/tag corrections via their feedback channels.

### Tier 6 — Cross-agent reach (~1 hour)

Because `SKILL.md` is a cross-compatible open standard, your one repo already works in:

| Agent | Install path |
|---|---|
| Claude Code | `claude plugin marketplace add jon-chun/deep-thoughts` |
| OpenAI Codex CLI | `codex skill add jon-chun/deep-thoughts` (verify current CLI syntax) |
| Cursor | Add via Cursor's skills panel pointing at the repo |
| VS Code Copilot | `code --install-extension` flow via the Agent Skills integration |
| Gemini CLI | Configure via its skills loader |
| OpenCode | Add repo URL to its skills config |
| Microsoft Agent Framework | Register via its Agent Skills directory |

Document each in your README under "Install". This isn't extra publishing work — it's just reminding users that the one repo works everywhere. It often doubles organic stars.

### Tier 7 — Curated awesome lists (wait ~2–4 weeks)

**Open a PR to `VoltAgent/awesome-agent-skills`** *after* your skill has visible community traction (stars, installs on skills.sh, a few forks, or external mentions). Their contributing guide explicitly rejects brand-new untested skills. Requirements on submission:
- Short description, ≤ 10 words
- Added under the correct subcategory in "Community Skills"
- Link must resolve

Opening the PR before traction exists wastes your shot. Use the waiting period to iterate on the description via your eval harness.

### Tier 8 — Optional / cautionary: ClawHub

**Only consider ClawHub if OpenClaw is an explicit target audience.** As of April 2026, ClawHub is recovering from the ClawHavoc attack; hundreds of malicious skills were removed and publisher requirements have tightened, but the reputational overhang remains and your work will sit alongside recently-purged malware. If you do publish:

```bash
clawhub skill publish ./deep-thoughts \
  --slug deep-thoughts \
  --name "Deep Thoughts" \
  --version 0.1.0 \
  --tags reasoning,socratic,design-thinking
```

Sign every release, pin dependencies, avoid any post-install hooks, and state in your README that the canonical source is GitHub. For a methodology skill (no executable payload), the security risk to *your users* is low; the risk to *your brand* is moderate. My recommendation is to **skip this tier unless you confirm measurable OpenClaw user demand.**

---

## 5. Launch-Day Amplification

Registry listings alone will not move the needle. Plan the announcement.

Draft a short "Show HN" post pointing at the repo. Lead with the demo transcript, not the description. HN readers respond to concrete before/after examples of how Socratic reasoning improved an actual decision.

Write a short post on your own site or Medium that: (a) motivates why Socratic prompting matters for AI research workflows (your stated domain), (b) shows 2–3 real transcripts, (c) explains the design of the description field and your eval harness. Mail a courtesy link to Simon Willison (simonw@simonwillison.net); his blog is a major discovery surface for Agent Skills.

Post in `r/ClaudeAI`, the Anthropic Discord `#agent-skills` or `#community-skills` channel, and one thread on X tagging `@AnthropicAI`, `@vercel`, and relevant AI-research accounts in your network.

If your skill is aligned with your stated research areas (multi-agent, ToM, machine psychology), cross-post to `r/LocalLLaMA`, `r/MachineLearning` (under guidelines), and the `ml-collective` or `eleutherai` Discords where methodology tools get thoughtful engagement.

---

## 6. Post-Launch Operations

Maintain semver discipline. Every behavior change to `SKILL.md` is a minor version bump; breaking changes (rename, description overhaul) are majors. Keep a real `CHANGELOG.md` — registry users look at it.

Re-run your eval harness on every release. Regressions in trigger accuracy are the most common failure mode.

Watch telemetry where you can get it: skills.sh install count, GitHub stars/forks/issues, Agensi dashboard stats, LobeHub view counts. Use the signal to decide whether it's worth customizing the description for specific registries (some let you override).

Respond to the first 10 issues personally and fast. Early responsiveness sets reputation.

After 4–6 weeks of organic usage, revisit: submit to `VoltAgent/awesome-agent-skills`, open the submission to `anthropics/claude-plugins-official`, and consider writing a "what I learned" post — those follow-up posts get far more organic installs than the launch post.

---

## 7. Special Notes for a Socratic / Design-Thinking Skill

Methodology skills face a different distribution problem than coding skills. Three tactical implications:

**Your users aren't scrolling the same leaderboards.** A product strategist, UX researcher, or AI researcher searching for a reasoning aid is unlikely to sort skills.sh by installs. They'll find you via blog posts, Twitter/X threads, podcasts, and word-of-mouth. Allocate more effort to Section 5 (amplification) and less to Section 4 (registry submissions) than a coding skill author would.

**Trigger terms must span vocabularies.** Engineers say "debug my thinking"; designers say "reframe the problem"; researchers say "steelman the null hypothesis"; executives say "stress-test this decision". Your 1,024-char description needs to carry at least one term from each vocabulary, or you will under-trigger for everyone but yourself.

**Pair it with a concrete example skill or workflow.** Pure-prompt skills are hard to evaluate. Bundle it with a second small skill that *uses* deep-thoughts for a concrete downstream task (e.g., `premortem-generator`, `assumption-audit`, `research-question-critic`). The companion skill drives installs of the parent.

---

## 8. Command Cheatsheet

```bash
# 0. One-time: install the skills CLI
npm install -g @vercel/skills
npm install -g docx                # if you ship a docx companion skill

# 1. Validate your SKILL.md against the spec
npx @agentskills/validate ./SKILL.md

# 2. Seed skills.sh telemetry
npx skills add jon-chun/deep-thoughts

# 3. Install via Claude Code plugin marketplace
claude plugin marketplace add jon-chun/deep-thoughts
claude plugin search @deep-thoughts
claude plugin install deep-thoughts@deep-thoughts

# 4. (Optional) Publish to ClawHub — see caveats in Section 4, Tier 8
clawhub skill publish ./ --slug deep-thoughts --name "Deep Thoughts" --version 0.1.0

# 5. Dry-run before any registry publish to catch accidental files
clawhub sync --dry-run
git status

# 6. Tag a release
git tag -a v0.1.0 -m "Initial public release"
git push origin v0.1.0
```

---

## 9. Two-Week Execution Plan

**Days 1–2.** Finalize `SKILL.md` description. Run 20-case eval harness. Write README with install commands for every supported agent. License + first tag.

**Day 3.** Publish GitHub repo public. Add plugin-marketplace manifest. Seed skills.sh via `npx skills add`. Ask 2–3 colleagues to install.

**Days 4–5.** Submit to Agensi.io and skillsdirectory.com. Allow security scans to complete.

**Day 6.** Launch post: Show HN, X thread, r/ClaudeAI, Anthropic Discord, courtesy note to Simon Willison.

**Days 7–14.** Respond to every issue and star. Monitor LobeHub/SkillsMP to confirm auto-indexing. Iterate description if trigger evals regress.

**Day 14+.** Submit PR to `VoltAgent/awesome-agent-skills`. Consider submission to `anthropics/claude-plugins-official`. Write retrospective post.

---

## 10. Sources

Every registry, feature claim, and submission flow above was verified against live sources on April 20, 2026.

- [anthropics/skills — Public repository for Agent Skills](https://github.com/anthropics/skills)
- [Agent Skills Specification](https://agentskills.io/specification)
- [Extend Claude with skills — Claude Code Docs](https://code.claude.com/docs/en/skills)
- [Skill authoring best practices — Claude API Docs](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- [Create and distribute a plugin marketplace — Claude Code Docs](https://code.claude.com/docs/en/plugin-marketplaces)
- [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official)
- [The Agent Skills Directory (skills.sh)](https://skills.sh/)
- [Introducing skills, the open agent skills ecosystem — Vercel changelog](https://vercel.com/changelog/introducing-skills-the-open-agent-skills-ecosystem)
- [vercel-labs/skills on GitHub](https://github.com/vercel-labs/skills)
- [Agensi AI Agent Skill Marketplace](https://www.agensi.io/)
- [How to Sell AI Agent Skills on Agensi (Creator Guide)](https://www.agensi.io/learn/how-to-sell-skills-on-agensi)
- [Skills Directory — Secure, Verified Agent Skills for Claude AI](https://www.skillsdirectory.com/)
- [SkillsMP — Agent Skills Marketplace](https://skillsmp.com/)
- [LobeHub Skills Marketplace](https://lobehub.com/skills)
- [VoltAgent/awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills)
- [VoltAgent/awesome-agent-skills CONTRIBUTING.md](https://github.com/VoltAgent/awesome-agent-skills/blob/main/CONTRIBUTING.md)
- [ClawHub — OpenClaw Docs](https://docs.openclaw.ai/tools/clawhub)
- [ClawHavoc Poisons OpenClaw's ClawHub With 1,184 Malicious Skills — Cyberpress](https://cyberpress.org/clawhavoc-poisons-openclaws-clawhub-with-1184-malicious-skills/)
- [Researchers Find 341 Malicious ClawHub Skills — The Hacker News](https://thehackernews.com/2026/02/researchers-find-341-malicious-clawhub.html)
- [ClawHavoc: Analysis — Antiy Labs](https://www.antiy.net/p/clawhavoc-analysis-of-large-scale-poisoning-campaign-targeting-the-openclaw-skill-market-for-ai-agents/)
- [Anthropic Opens Agent Skills Standard — Unite.AI](https://www.unite.ai/anthropic-opens-agent-skills-standard-continuing-its-pattern-of-building-industry-infrastructure/)
- [Agent Skills — Simon Willison (Dec 19, 2025)](https://simonwillison.net/2025/Dec/19/agent-skills/)
- [Agent Skills — Codex | OpenAI Developers](https://developers.openai.com/codex/skills)
- [Use Agent Skills in VS Code](https://code.visualstudio.com/docs/copilot/customization/agent-skills)
