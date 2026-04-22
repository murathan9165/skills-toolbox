# Changelog

All notable changes to this repository will be documented in this file.

Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) · Versioning: [SemVer](https://semver.org/).

## [0.1.0] — 2026-04-22

### Added
- Initial public release of `skills-toolbox` as a multi-skill `SKILL.md` monorepo.
- `docs/tech-spec.md` — authoritative authoring + publishing spec.
- `docs/deep-thoughts-publishing-strategy.md` — registry deep-dive (pre-existing).
- `skills/deep-thoughts/` — Socratic / design-thinking reasoning skill (v0.1.0).
- `.claude-plugin/marketplace.json` — Claude Code plugin marketplace manifest.
- `skills.json` — skills.sh bundle manifest.
- TDD test suite (`tests/unit`, `tests/integration`, `tests/e2e`) with description-heuristic checks.
- GitHub Actions CI (`.github/workflows/ci.yml`).
- `pyproject.toml` with `uv`-managed dev dependencies.
