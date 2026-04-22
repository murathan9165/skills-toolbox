# Contributing to `skills-toolbox`

Thank you for wanting to contribute a skill. Please read [`docs/tech-spec.md`](docs/tech-spec.md) first — it is the authoritative spec.

## TL;DR — Adding a new skill

1. **Fork and branch.** `git checkout -b skill/<name>`.
2. **Create `skills/<name>/`** following the canonical layout in tech-spec §3.
3. **Write `SKILL.md`** with frontmatter per tech-spec §4. Description must be triggering-only (starts with "Use when …"), ≤ 1024 chars, third person.
4. **Add `.claude-plugin/plugin.json`** mirroring the SKILL.md frontmatter.
5. **Add `evals/trigger-tests.json`** with ≥ 20 cases and both polarities represented (≥ 30% each).
6. **List your skill** in `.claude-plugin/marketplace.json` and `skills.json`.
7. **Add a row** to the catalog table in top-level `README.md`.
8. **Run tests:** `uv run pytest tests/ -v` until green.
9. **Add CHANGELOG entries** at the skill level and at the repo level.
10. **Open a PR.** Title: `feat(<skill-name>): brief description`.

## Description engineering checklist

Tests in `tests/e2e/test_description_heuristics.py` enforce these rules. Read `superpowers:writing-skills` for background.

- [ ] Starts with `Use when …`
- [ ] Describes triggers, not what the skill does
- [ ] Third person only (no "I", "we", "our", "my")
- [ ] ≥ 4 distinct trigger phrases / keywords
- [ ] Includes vocabulary from at least 2 of: engineer / designer / researcher / executive
- [ ] ≤ 1024 characters
- [ ] No XML tags, no markdown formatting

## Testing philosophy

- **Unit:** per-skill structural checks (frontmatter, plugin.json).
- **Integration:** cross-manifest consistency.
- **E2E:** catalog completeness, description heuristics, eval-harness integrity.
- **Live (`pytest -m live`):** optional LLM accuracy tests; not required for PR merge.

Tests use pytest with parametrization over discovered skills. A new skill that follows the canonical layout is automatically included in the unit/integration/e2e suites.

## Commit style

- `feat(<skill>): …` for new skills or added methods
- `fix(<skill>): …` for bug fixes, description tuning, trigger-eval corrections
- `docs: …` for README / tech-spec changes
- `test: …` for test-only changes
- `chore: …` for tooling, CI, dependencies

Keep commits small and atomic. Every commit should leave `uv run pytest tests/` green.

## Versioning

[Semantic versioning](https://semver.org/) at both repo and skill level:

- Description rewrites → minor bump (behavior change)
- Added methods / references → minor bump
- Structural breaking changes (rename, removed method) → major bump
- Typo fixes, non-trigger docs → patch bump

## Licensing

By submitting a contribution, you agree it will be released under the repo's MIT license. If your skill bundles third-party content, include proper attribution in the skill's own `README.md`.
