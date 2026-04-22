# deep-thoughts

A Socratic and design-thinking reasoning companion for Claude Code and compatible agents.

Slow down before answering. Surface assumptions. Reframe the question. Run a premortem. Steelman the opposing view. Apply first-principles. Then produce a recommendation with explicit confidence and a cheapest-falsifier test.

## When it triggers

Any request where jumping straight to a solution would skip important questions:

- Strategic / product / research decisions with unclear success criteria
- "Should I / what should we / help me think through" prompts
- Plans that feel obviously right (overconfidence is a trigger)
- Hiring, ethics, irreversible tradeoffs
- Recurring-symptom debugging where root cause is unclear

## Install

```bash
# Claude Code (plugin marketplace)
claude plugin marketplace add jon-chun/skills-toolbox
claude plugin install deep-thoughts@skills-toolbox

# Any SKILL.md-compatible agent (project scope)
# Copy skills/deep-thoughts/ into your project's .claude/skills/ or equivalent.
```

## What's inside

- `SKILL.md` — the skill itself (frontmatter + workflow)
- `references/` — progressive-disclosure method docs, loaded only when a method is applied
  - `socratic-question-ladder.md`
  - `five-whys.md`
  - `premortem-template.md`
  - `steelman-and-double-crux.md`
  - `first-principles-decomposition.md`
  - `assumption-audit.md`
- `evals/trigger-tests.json` — 24 cases used to tune the description
- `CHANGELOG.md` — semver history for this skill

## Design notes

- **Description is triggering-only**, not a workflow summary. This avoids the Claude shortcut where the description becomes the whole skill.
- **1,024-character cap** on the description field is enforced by the repo's CI.
- **Vocabulary spread** in the description covers engineer ("debug my thinking"), designer ("reframe"), researcher ("steelman hypothesis"), and executive ("stress-test this decision") phrasings.
- **Progressive disclosure** — methods live in `references/` so the SKILL.md body stays short; the agent loads a method file only when applying that method.

## License

MIT — see `/LICENSE` at the repo root.
