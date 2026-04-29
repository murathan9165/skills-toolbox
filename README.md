# skills-toolbox

> Jon Chun's curated Agent Skills toolbox — `SKILL.md`-format skills that work across Claude Code, OpenAI Codex, Cursor, VS Code Copilot, Gemini CLI, and other `SKILL.md`-compatible agents.

[![CI](https://github.com/jon-chun/skills-toolbox/actions/workflows/ci.yml/badge.svg)](https://github.com/jon-chun/skills-toolbox/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Spec: Agent Skills](https://img.shields.io/badge/spec-agentskills.io-informational)](https://agentskills.io/specification)

---

## What is this?

A monorepo of small, composable **agent skills**. Each skill is a folder containing a `SKILL.md` file plus optional references, scripts, and evals. Any `SKILL.md`-aware agent can install them individually or in bulk.

The toolbox is **authoring-quality first, publishing-reach second**. Every skill ships with:

- A triggering-only description (≤ 1024 chars, per the spec)
- Progressive-disclosure reference docs (loaded only when the method is applied)
- A trigger-eval harness (≥ 20 should / shouldn't cases)
- A Claude Code plugin manifest (`.claude-plugin/plugin.json`)
- CI that validates every commit

See [`docs/tech-spec.md`](docs/tech-spec.md) for the complete authoring and publishing spec.

---

## Catalog

| Skill | What it does | Version |
|---|---|---|
| [`deep-thoughts`](skills/deep-thoughts/) | Socratic / design-thinking companion — reframes, surfaces assumptions, runs premortems, steelmans, applies first-principles | 0.1.0 |

More skills coming. See [CONTRIBUTING.md](CONTRIBUTING.md) for how to add one.

---

## Install

### Claude Code (plugin marketplace — recommended)

```bash
# Add the marketplace once
claude plugin marketplace add jon-chun/skills-toolbox

# Install individual skills (each is exposed as its own plugin)
claude plugin install deep-thoughts@skills-toolbox
```

Verify with `claude plugin list` — `deep-thoughts@skills-toolbox` should appear with status `enabled`. The marketplace and every plugin manifest pass `claude plugin validate` in CI.

### skills.sh (Vercel Labs)

```bash
npx skills add jon-chun/skills-toolbox
```

### Project-scoped install (any `SKILL.md`-compatible agent)

Copy the skill folder into your project's skill directory:

```bash
# Claude Code
cp -R skills/deep-thoughts .claude/skills/

# OpenAI Codex
cp -R skills/deep-thoughts .codex/skills/

# Cursor, VS Code Copilot, Gemini CLI — see each agent's docs
```

### Cross-agent install paths

| Agent | Command |
|---|---|
| Claude Code | `claude plugin marketplace add jon-chun/skills-toolbox` |
| OpenAI Codex CLI | `codex skill add jon-chun/skills-toolbox` *(verify current syntax)* |
| Cursor | Cursor → Skills panel → Add repo URL |
| VS Code Copilot | Agent Skills integration → Install from repo |
| Gemini CLI | Configure via `~/.gemini/config` skills loader |
| OpenCode | Add repo URL to skills config |
| Project-scope | Copy `skills/<name>/` into project's `.claude/skills/` or equivalent |

---

## Repo layout

```
skills-toolbox/
├── README.md                       # You are here
├── docs/
│   ├── tech-spec.md                # Authoring + publishing spec — read first if contributing
│   └── …
├── skills/
│   └── deep-thoughts/              # One skill per subfolder; canonical Anthropic layout
│       ├── SKILL.md                # Required: frontmatter + instructions
│       ├── README.md
│       ├── CHANGELOG.md
│       ├── .claude-plugin/plugin.json   # Per-skill metadata (also passes `claude plugin validate`)
│       ├── references/             # Progressive-disclosure method docs
│       ├── scripts/                # Optional tools (Python here)
│       └── evals/trigger-tests.json
├── .claude-plugin/
│   └── marketplace.json            # Marketplace manifest. Each plugin uses
│                                   #   source: "./", skills: ["./skills/<name>"], strict: false
│                                   # so Claude Code's loader resolves SKILL.md correctly.
├── skills.json                     # skills.sh bundle manifest
├── tests/                          # unit / integration / e2e + official-validator e2e
├── pyproject.toml                  # uv-managed dev deps
└── .github/workflows/ci.yml        # Validates every commit
```

> **Marketplace layout note.** Earlier versions declared each plugin with
> `source: "./skills/<name>"` (no `skills` array). That fails Claude Code's
> plugin loader, which expects skills at `<source>/skills/<name>/SKILL.md` by
> default — so the plugin would install with zero skills. The current layout
> mirrors `anthropic-agent-skills`: one shared source (`./`) plus an explicit
> `skills` path per plugin. See `tests/integration/test_plugin_loader_simulation.py`
> for the regression test.

---

## Development

This repo uses [`uv`](https://docs.astral.sh/uv/) for Python tooling (per `CLAUDE.md`). No runtime Python is required to *use* the skills — Python is only for the test harness.

```bash
# Install dev dependencies
uv sync --group dev

# Run the full test suite (unit + integration + e2e)
uv run pytest tests/ -v

# Lint + format
uv run ruff check . --fix
uv run ruff format .
```

CI runs the same commands on every push. Failing tests block merges.

### Adding a new skill

Short version: follow the checklist in [`docs/tech-spec.md §11`](docs/tech-spec.md#11-adding-a-new-skill--checklist).

Long version: see [CONTRIBUTING.md](CONTRIBUTING.md).

---

## Testing philosophy

Three layers, all static (no network / API calls in default CI):

| Layer | What it checks |
|---|---|
| **Unit** (`tests/unit/`) | Per-skill: frontmatter shape, `name` regex, description length, plugin manifest fields |
| **Integration** (`tests/integration/`) | Cross-manifest consistency: SKILL.md ↔ plugin.json ↔ marketplace.json ↔ skills.json |
| **E2E** (`tests/e2e/`) | Repo-level: catalog completeness, trigger-eval integrity, description heuristics |

An optional **live** layer (`pytest -m live`) runs trigger evals against a real LLM; opt-in because it costs money.

---

## Publishing

See [`docs/tech-spec.md §8`](docs/tech-spec.md#8-publishing-workflow) for the full matrix.

Short version:

1. Ship to GitHub (this repo).
2. Wire up Claude Code plugin marketplace (done).
3. Seed `skills.sh` telemetry (`npx skills add jon-chun/skills-toolbox`).
4. Submit to Agensi.io + skillsdirectory.com.
5. Let SkillsMP / LobeHub auto-crawl.
6. Wait 2–4 weeks, then PR to `VoltAgent/awesome-agent-skills`.
7. ClawHub is intentionally skipped — see the spec doc for why.

---

## Acknowledgements

- [Anthropic](https://www.anthropic.com/) for open-sourcing the Agent Skills standard (Dec 2025).
- Contributors to `anthropics/skills`, `vercel-labs/skills`, and `VoltAgent/awesome-agent-skills` for reference examples.
- Simon Willison for writing about Agent Skills early and often.

---

## License

MIT — see [LICENSE](LICENSE).

The prose content of skills (reference docs, method descriptions) is also offered under MIT unless a per-skill README states otherwise.

---

## Author

Jon Chun — [github.com/jon-chun](https://github.com/jon-chun)

Issues and PRs welcome.
