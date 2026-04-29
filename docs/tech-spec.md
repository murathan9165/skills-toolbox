# Tech Spec — `jon-chun/skills-toolbox`

**A multi-skill monorepo for Agent Skills (`SKILL.md`) compatible with Claude Code, OpenAI Codex, Cursor, VS Code Copilot, Gemini CLI, and other `SKILL.md` consumers.**

- Author: Jon Chun (`jon-chun`)
- Date: 2026-04-22
- Status: v1 — governs repo structure, skill authoring, testing, CI, and publishing
- Canonical source: `github.com/jon-chun/skills-toolbox`

---

## 1. Purpose & scope

This document tells an engineer (human or agent) exactly how to add a new skill to this repo and ship it without breaking the toolbox. It covers:

- Repo layout and manifest files
- `SKILL.md` authoring rules (the 1,024-character fight, naming regex, progressive disclosure)
- TDD testing strategy (unit / integration / e2e / optional trigger-evals)
- CI gates
- Publishing workflow across registries, with honest risk ratings
- Cross-agent install paths

It does **not** cover skill-specific methodology (live inside each `skills/<name>/` folder).

---

## 2. Critique of the supplied Grok setup doc

The supplied `docs/chat_github-setup_grok_RAW_20260421.md` is directionally right — monorepo + GitHub-first + the five named registries — but it has several errors and omissions that would cost time or reputation if followed verbatim. The prior `docs/deep-thoughts-publishing-strategy.md` caught the biggest ones (ClawHub/ClawHavoc, plugin marketplaces, description engineering, eval harness, awesome-list gating, announcement surface). The additional issues below complete the picture.

### 2.1 Factual errors / unverifiable claims

1. **ClawHub is top-recommended with no mention of ClawHavoc.** The Jan–Feb 2026 supply-chain attack flooded ClawHub with 341–900+ malicious skills. Publishing there now is a brand risk for a methodology skill; the doc is silent. *(Strategy doc caught this.)*
2. **"~87k+ unique skills on skills.sh"** is not a verified figure. The platform publishes install counts, not a unique-skill total.
3. **"80/20 revenue split on Agensi"** is not substantiated in current public docs; treat monetization terms as "check the dashboard".
4. **"OpenClaw has 220k stars"** appears only in one promotional blog; not a primary source.
5. **"LobeHub ~280k+" and "SkillsMP hundreds of thousands"** conflate aggregator crawl indexes with active-skill counts.
6. **"Vercel" attribution for skills.sh** should be **Vercel Labs** (the experimental arm); they are not the same group inside Vercel.
7. **`npx skills add <github-url>`** is cited as if it both *installs* and *registers*. In practice it installs locally and emits telemetry; there is no separate submission form. That detail matters for a launch plan.

### 2.2 Technical errors

8. **Conflates `skills.json` with the Claude Code plugin manifest.** These are different files for different platforms:
   - Claude Code: `.claude-plugin/plugin.json` (per-plugin) and `.claude-plugin/marketplace.json` (repo-level marketplace).
   - skills.sh: its own `skills.json` bundle manifest.
   - Neither is "the" manifest. Both should exist in a toolbox repo.
9. **Doesn't mention `name` field regex.** The spec allows only letters, numbers, and hyphens — no parentheses, spaces, or underscores. Skill names that violate this silently fail to install on some agents.
10. **"Each skill in its own subfolder" without mentioning `skills/<name>/SKILL.md` vs repo-root `SKILL.md`.** Both are valid but imply different install mechanics. A toolbox should use subfolders.
11. **No mention of `.claude/skills/` project-scope installs.** Users can drop a repo's skills into a project `.claude/skills/` path without installing a plugin. This is a legitimate cross-agent pattern.

### 2.3 Critical omissions

12. **Claude Code plugin marketplaces.** First-party Anthropic distribution (`claude plugin marketplace add <repo>`). Missing entirely. *(Strategy doc caught this.)*
13. **The `description` field is the entire trigger signal.** Spec cap: 1,024 characters. Claude under-triggers skills when descriptions summarize workflow instead of describing triggering conditions. The doc says "follow the spec" without this load-bearing detail. *(Strategy doc caught this.)*
14. **No eval harness / trigger tests.** A skill that never fires is invisible regardless of where it is listed. *(Strategy doc caught this.)*
15. **No CI gate for `SKILL.md` validity.** Every commit should validate frontmatter, description length, and manifest cross-references. The doc mentions "optional CI" but specifies nothing.
16. **No semver discipline.** Description rewrites are behavior changes; treat them as version bumps.
17. **No cross-agent install table.** The doc says "works everywhere" but lists no install commands for Codex, Cursor, Copilot, Gemini, OpenCode.
18. **No security checklist.** Skills with `scripts/` can run code on install in some harnesses. Zero mention of post-install hook risks, secret scanning, or dependency pinning.
19. **No announcement surface.** Skill adoption is driven by Simon Willison, Hacker News, Anthropic Discord, r/ClaudeAI as much as by registry listings. *(Strategy doc caught this.)*
20. **No `VoltAgent/awesome-agent-skills` maturity gate.** Submitting a brand-new skill gets rejected; wait 2–4 weeks. *(Strategy doc caught this.)*
21. **No description-keyword vocabulary spread.** Methodology skills need terms from engineering, product, research, and executive vocabularies or they under-trigger outside their native lane. *(Strategy doc caught this.)*
22. **No pairing / companion-skill strategy.** Pure-prompt skills drive more installs when paired with a concrete downstream skill.

### 2.4 Net

The Grok doc gets publishing 80% right and authoring 30% right. The authoring gap is what sinks skills. This spec fixes the authoring gap first, then treats publishing as a downstream concern.

---

## 3. Repo layout (canonical)

```
skills-toolbox/
├── README.md                          # Human-facing front page, install matrix, skill catalog
├── CHANGELOG.md                       # Toolbox-level semver history
├── CONTRIBUTING.md                    # How to add a new skill (checklist)
├── LICENSE                            # MIT (or Apache-2.0)
├── pyproject.toml                     # uv-managed Python deps (pytest, pyyaml, jsonschema)
├── .gitignore
├── .claude-plugin/
│   └── marketplace.json               # Marketplace manifest (Claude Code)
├── skills.json                        # skills.sh bundle manifest
├── skills/
│   └── <skill-name>/                  # ONE skill per subfolder (hyphenated, short)
│       ├── SKILL.md                   # REQUIRED: YAML frontmatter + instructions
│       ├── README.md                  # Optional but recommended: human-facing
│       ├── CHANGELOG.md               # Per-skill semver history
│       │                              # NOTE: NO .claude-plugin/plugin.json here.
│       │                              # Per-skill plugin.json conflicts with the
│       │                              # marketplace entry (see §5.1).
│       ├── references/                # Progressive-disclosure reference docs (loaded on demand)
│       │   └── *.md
│       ├── scripts/                   # Optional executable helpers (language-agnostic)
│       ├── assets/                    # Optional templates, prompts, examples
│       └── evals/
│           └── trigger-tests.json     # Should/shouldn't-trigger eval cases (≥20)
├── tests/
│   ├── __init__.py
│   ├── conftest.py                    # Shared fixtures (skill discovery)
│   ├── unit/                          # Per-skill structural checks
│   ├── integration/                   # Cross-manifest consistency
│   └── e2e/                           # Repo-level catalog + description heuristics
├── scripts/
│   └── validate_skills.py             # CLI that runs the same checks CI runs
├── .github/
│   └── workflows/
│       └── ci.yml                     # Runs validate_skills + pytest on every push
└── docs/
    ├── tech-spec.md                   # (this document)
    ├── chat_github-setup_grok_RAW_20260421.md
    └── deep-thoughts-publishing-strategy.md
```

**Rationale.** Each skill is also a Claude Code plugin, so end users can install one skill at a time (`claude plugin install <skill>@skills-toolbox`) without pulling the whole toolbox. The top-level `marketplace.json` declares this repo as a marketplace; `skills.json` lets `skills.sh` bundle-install everything. Both file formats are required by their respective platforms; do not conflate them.

---

## 4. `SKILL.md` authoring rules

### 4.1 Frontmatter

Required fields per the `agentskills.io` spec: `name`, `description`. All others are optional but recommended.

```yaml
---
name: deep-thoughts                              # letters, numbers, hyphens only; ≤ 64 chars
description: |
  Use when ...                                  # third-person, triggers only, ≤ 1024 chars
version: 0.1.0                                   # semver; bump on behavior change
author: jon-chun
license: MIT
homepage: https://github.com/jon-chun/skills-toolbox
keywords: [reasoning, socratic, design-thinking] # searchable terms for registries
---
```

**Hard rules enforced in CI:**
- `name`: matches `^[a-z][a-z0-9-]{1,63}$` (lowercase, starts with letter, hyphens allowed).
- `description`: 1 ≤ len ≤ 1024 characters. No XML tags.
- Frontmatter YAML must parse.
- Total frontmatter block ≤ 1024 characters is a **spec** rule — CI checks description length; frontmatter overall is informally capped but not enforced.

### 4.2 Description engineering (the single highest-ROI decision)

The description is injected into every downstream agent's system prompt. It is the sole signal used to decide whether to load the skill. Anthropic's guidance: agents under-trigger. Write descriptions that are triggering-focused, not workflow-summarizing.

**Do:**
- Start with `Use when …`.
- List concrete triggering situations, phrases, and symptoms.
- Include vocabulary from multiple user personas where the skill applies (engineer, designer, researcher, executive).
- Write in third person.

**Don't:**
- Summarize what the skill does or how it works. If the description says "Guides the agent through X", Claude often follows the description instead of reading the body.
- Use first person ("I help with...").
- Use placeholders, generic phrases ("for async testing").
- Include XML tags or markdown syntax.

**Length target:** ~500–900 characters. Hard cap 1,024 by spec; longer descriptions get truncated in some registries.

### 4.3 Body structure

Follow this template (tune sections per skill type):

```markdown
# <Skill Title>

## Overview
Core principle in 1–2 sentences.

## When to use
Concrete triggers (bullets). When NOT to use.

## Quick reference
Scannable table or bulleted methods.

## Workflow
Numbered steps or state diagram.

## References
Links to files in `references/` (loaded on demand).

## Common mistakes
What goes wrong and how to recover.
```

Keep the SKILL.md body under ~500 words where possible. Push long reference material into `references/` so it loads only when needed (progressive disclosure).

### 4.4 Progressive disclosure

Anything over ~100 lines of reference material goes in `references/<topic>.md`, linked from SKILL.md with a clear "load this when …" hint. Heavy references are the #1 source of wasted context.

---

## 5. Plugin & marketplace manifests

### 5.1 Per-skill `plugin.json` — DO NOT ADD

> **Hard rule.** Do not place `.claude-plugin/plugin.json` inside any
> `skills/<name>/` directory. Claude Code's loader treats a per-skill
> plugin.json as a second component-declaring manifest, conflicting with the
> marketplace's `skills: [...]` entry, and `claude /doctor` reports:
>
> > Plugin <name> has conflicting manifests: both plugin.json and
> > marketplace entry specify components.
>
> All plugin metadata (`name`, `version`, `description`, `author`, `license`,
> `keywords`, `repository`, `homepage`) lives in the marketplace.json plugin
> entry instead. CI enforces this with
> `tests/unit/test_skill_structure.py::test_skill_has_no_per_skill_plugin_manifest`
> and `tests/integration/test_plugin_loader_simulation.py::test_strict_false_skills_paths_have_no_sibling_plugin_json`.

The proven-good layout (`anthropic-agent-skills`) ships zero per-skill
plugin.json files. SKILL.md frontmatter remains the source of truth for
skill identity, and the marketplace entry is the source of truth for plugin
distribution metadata.

> **Schema gotcha — `repository` must be a string.** When set on the
> marketplace entry, Claude Code's plugin schema requires
> `repository: "<url>"` (not the npm-style
> `{ "type": "git", "url": "...", "directory": "..." }` object). Object-form
> repository fields fail `claude plugin validate` with
> `repository: Invalid input: expected string, received object`.

### 5.2 `.claude-plugin/marketplace.json` (repo root)

```json
{
  "name": "skills-toolbox",
  "owner": { "name": "jon-chun", "url": "https://github.com/jon-chun" },
  "plugins": [
    {
      "name": "deep-thoughts",
      "source": "./",
      "skills": ["./skills/deep-thoughts"],
      "strict": false,
      "version": "0.1.0",
      "description": "Socratic and design-thinking reasoning skill."
    }
  ]
}
```

**Why this shape (and not `source: "./skills/<name>"`).** Claude Code's
plugin loader discovers skills at `<source>/skills/<name>/SKILL.md` by
default. Pointing `source` directly at a skill folder would make the loader
look for `skills/deep-thoughts/skills/<name>/SKILL.md` — which doesn't
exist, so the plugin installs with zero skills. The canonical fix (used by
`anthropic-agent-skills`) is to set `source: "./"` and override discovery
with an explicit `skills` array. `strict: false` then tells Claude Code the
marketplace entry — not a per-source `plugin.json` — is authoritative for
component definitions.

Per-skill `skills/<name>/.claude-plugin/plugin.json` is **deliberately
absent** — see §5.1. For project-scope installs (copy a skill folder into a
project's `.claude/skills/`), the SKILL.md frontmatter alone is sufficient;
no per-skill plugin.json is required by Claude Code or any other
SKILL.md-compatible agent.

Users install with:
```bash
claude plugin marketplace add jon-chun/skills-toolbox
claude plugin install deep-thoughts@skills-toolbox
```

### 5.3 `skills.json` (repo root) — skills.sh bundle

```json
{
  "name": "jon-chun/skills-toolbox",
  "version": "0.1.0",
  "description": "Jon Chun's agent skills toolbox.",
  "skills": [
    { "name": "deep-thoughts", "path": "skills/deep-thoughts",
      "description": "Socratic and design-thinking reasoning skill." }
  ]
}
```

Install via:
```bash
npx skills add jon-chun/skills-toolbox
```

Format details should be re-verified against `skills.sh` docs before publishing; registries evolve.

---

## 6. Testing strategy (TDD)

Three layers, all run in CI. Python is used as the test host because it is already the toolbox language (per `CLAUDE.md`); no runtime dependency on Python leaks into the skills themselves.

### 6.1 Unit tests (`tests/unit/`)

Structural checks on each skill in isolation:
- `test_skill_frontmatter.py` — YAML parses; required fields present; `name` regex; `description` length bounds.
- `test_skill_structure.py` — required files exist (`SKILL.md`, `README.md` if declared, `evals/trigger-tests.json`).
- `test_plugin_manifest.py` — each skill's marketplace plugin entry parses and has required fields (per-skill `plugin.json` was removed; see §5.1).

### 6.2 Integration tests (`tests/integration/`)

Cross-file consistency:
- `test_marketplace_manifest.py` — `marketplace.json` parses; every listed plugin `source` directory exists and contains `SKILL.md`.
- `test_skills_manifest.py` — `skills.json` parses; every listed skill path exists.
- `test_manifests_consistent.py` — skill `name` and `version` match across SKILL.md frontmatter, `marketplace.json`, and `skills.json`.

### 6.3 E2E tests (`tests/e2e/`)

Repo-level / user-facing:
- `test_skill_catalog.py` — every `skills/*/` subdir is listed in top-level `README.md`, `marketplace.json`, AND `skills.json` (no orphans).
- `test_trigger_evals.py` — each skill's `evals/trigger-tests.json` has ≥ 20 cases with a sane should/shouldn't mix (≥ 30% of each polarity).
- `test_description_heuristics.py` — description starts with `Use when`, is third-person (no `I `/`we `), includes ≥ 4 distinct trigger terms, stays within 1,024 chars.

### 6.4 Optional: live trigger evals

A second, opt-in layer (`tests/live/`, `pytest -m live`) can drive an actual LLM against each `evals/trigger-tests.json` and measure should/shouldn't accuracy. Excluded from default CI because it requires an API key and costs money; expected to be run manually before description rewrites.

### 6.5 TDD discipline

Adding or editing a skill follows RED-GREEN:
1. Write (or update) the relevant test that expresses the new expectation.
2. Run pytest, confirm the test fails.
3. Make the smallest change to SKILL.md / manifest / reference file that makes the test pass.
4. Commit both test and fix in one commit.

---

## 7. CI

`.github/workflows/ci.yml` runs on every push and PR:

1. Check out repo.
2. Install uv + Python 3.12.
3. `uv sync`.
4. `uv run pytest tests/ -v --tb=short`.
5. (Optional) `uv run python scripts/validate_skills.py` for a human-readable report.

Failing CI blocks merges to `main`. Releases are tagged `v<semver>` after CI passes.

---

## 8. Publishing workflow

Per-skill workflow, aligned with the critique in Section 2:

### 8.1 Pre-flight

1. All CI green on `main`.
2. SKILL.md description iterated against `evals/trigger-tests.json`.
3. `CHANGELOG.md` entry added at skill and repo level.
4. Tag `git tag -a v<semver>` and push.

### 8.2 Publishing matrix (by ROI, honest-risk-rated)

| # | Target | Cost | Reach | Risk | Action |
|---|--------|------|-------|------|--------|
| 1 | GitHub (this repo) | 0 | Foundational | None | `git push` + tag release |
| 2 | Claude Code plugin marketplace | 1h one-time | High (Claude-native users) | None | Add `marketplace.json`; instruct users `claude plugin marketplace add jon-chun/skills-toolbox` |
| 3 | skills.sh (Vercel Labs) | 10m | High (telemetry-driven leaderboard) | Low | Add `skills.json`; seed telemetry with `npx skills add jon-chun/skills-toolbox` from 2–3 clean machines |
| 4 | Agensi.io | 30m | Medium (curated marketplace) | Low | Submit repo; allow automated security scan |
| 5 | skillsdirectory.com | 30m + wait | Medium (manually reviewed) | None | Sign in with GitHub at `skillsdirectory.com/submit` |
| 6 | SkillsMP.com / LobeHub | 0 | Medium (auto-crawled) | None | Do nothing; public repo gets crawled |
| 7 | `anthropics/claude-plugins-official` | Wait, then submit | High-credibility | None | Submit only after real adoption |
| 8 | `VoltAgent/awesome-agent-skills` | PR after 2–4 weeks | Curated, high-trust | None | Brand-new skills are rejected; wait for community traction |
| 9 | ClawHub | Optional | Niche | **Reputational** | Skip unless OpenClaw is an explicit target audience; note the ClawHavoc fallout |

### 8.3 Announcement surface

On launch day, post to: Show HN, X (tag `@AnthropicAI`), r/ClaudeAI, Anthropic Discord `#community-skills`, courtesy email to Simon Willison. Registry listings alone rarely move the needle.

---

## 9. Cross-agent install paths

One repo, many agents. Document each in the top-level `README.md`:

| Agent | Install path |
|---|---|
| Claude Code | `claude plugin marketplace add jon-chun/skills-toolbox && claude plugin install <skill>@skills-toolbox` |
| OpenAI Codex CLI | `codex skill add jon-chun/skills-toolbox` (verify current syntax) |
| Cursor | Cursor → Skills panel → Add repo URL |
| VS Code Copilot | `code --install-extension` flow via Agent Skills integration |
| Gemini CLI | Configure via skills loader in `~/.gemini/config` |
| OpenCode | Add repo URL to skills config |
| Project-scope (any agent) | Copy `skills/<name>/` into project's `.claude/skills/` (or equivalent) |

All of these are zero-cost because SKILL.md is the same file across agents.

---

## 10. Security checklist (per skill)

- [ ] No secrets or API keys in SKILL.md, scripts, or references.
- [ ] `scripts/` contents are reviewed; no post-install hooks that execute on `add`.
- [ ] External URLs are pinned and HTTPS.
- [ ] Dependencies (if any) are pinned in a manifest.
- [ ] License file present.
- [ ] Signed git tag for releases (`git tag -s`).
- [ ] No binary artifacts > 1 MB (use Git LFS or external storage).

---

## 11. Adding a new skill — checklist

1. Create `skills/<name>/` following the layout in Section 3.
2. Write SKILL.md with frontmatter per Section 4; keep description under 1,024 chars and triggering-only.
3. Add a plugin entry to `.claude-plugin/marketplace.json` (`source: "./"`, `skills: ["./skills/<name>"]`, `strict: false`, plus name/version/description/keywords). Do **not** add a per-skill `.claude-plugin/plugin.json` — see §5.1.
4. Add `evals/trigger-tests.json` with ≥ 20 cases.
5. Add the skill to `skills.json`.
6. Add a catalog entry to `README.md`.
7. Run `uv run pytest tests/` until green; verify with `claude plugin validate .` and a real `claude plugin install <name>@skills-toolbox` round-trip.
8. Add a `CHANGELOG.md` entry (skill-level and repo-level).
9. Commit, push, tag release.

---

## 12. Open questions & future work

- **Signed skill releases.** Skill supply-chain security (post-ClawHavoc) will likely demand signed releases. Investigate `sigstore` / `cosign` for skill tarballs.
- **Per-registry description overrides.** Some registries allow longer or differently-tuned descriptions. Build a `descriptions/<registry>.yaml` override mechanism when needed.
- **Live trigger-eval harness.** Wire up a `pytest -m live` target that calls an LLM to evaluate trigger accuracy.
- **Skill dependency declarations.** When skills reference each other (e.g., `premortem-generator` depends on `deep-thoughts`), introduce a `requires:` field and CI-enforce resolution.

---

## 13. References

- Agent Skills spec: `https://agentskills.io/specification`
- Claude Code plugin marketplaces: `https://code.claude.com/docs/en/plugin-marketplaces`
- Claude skills docs: `https://code.claude.com/docs/en/skills`
- skills.sh: `https://skills.sh/`
- `vercel-labs/skills` (reference repo)
- `anthropics/skills` (first-party examples)
- `anthropics/claude-plugins-official` (curated plugin directory)
- `VoltAgent/awesome-agent-skills` (curated awesome list, with contribution gate)
- Internal: `docs/deep-thoughts-publishing-strategy.md` (registry-by-registry deep-dive)
