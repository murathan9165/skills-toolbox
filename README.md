# skills-toolbox

> Murathan Kocaman's curated Agent Skills toolbox — `SKILL.md`-format skills that work across Claude Code, OpenAI Codex, Cursor, VS Code Copilot, Gemini CLI, and other `SKILL.md`-compatible agents.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Spec: Agent Skills](https://img.shields.io/badge/spec-agentskills.io-informational)](https://agentskills.io/specification)

---

## What is this?

A monorepo of composable **agent skills** built around projects from IPHS 300 AI for Humanity at Kenyon College. Each skill is a folder containing a `SKILL.md` file plus optional references, scripts, and evals. Any `SKILL.md`-aware agent can install them individually or in bulk.

---

## Catalog

| Skill | What it does | Version |
|---|---|---|
| [`nonprofit-grant-writing`](skills/nonprofit-grant-writing/) | Structured grant proposal workflow for nonprofits — enforces research-first sequencing, SMART objectives, logic model, budget justification discipline, and Red Team 5 Cs review | 1.0.0 |

---

## Install

### Project-scoped install (any `SKILL.md`-compatible agent)

```bash
# Claude Code
cp -R skills/nonprofit-grant-writing .claude/skills/

# OpenAI Codex
cp -R skills/nonprofit-grant-writing .codex/skills/
```

### skills.sh

```bash
npx skills add murathan9165/skills-toolbox
```

---

## Repo layout

```
skills-toolbox/
├── README.md
├── skills/
│   └── nonprofit-grant-writing/    # One skill per subfolder
│       └── SKILL.md                # Required: frontmatter + instructions
├── skills.json                     # skills.sh bundle manifest
└── LICENSE
```

---

## License

MIT — see [LICENSE](LICENSE).

---

## Author

Murathan Kocaman — [github.com/murathan9165](https://github.com/murathan9165)
