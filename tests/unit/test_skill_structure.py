"""Unit tests: each skill directory follows the canonical layout in tech-spec.md."""

from __future__ import annotations

from tests.conftest import Skill


def test_skill_has_skill_md(skill: Skill) -> None:
    assert skill.skill_md_path.exists()
    assert skill.skill_md_path.is_file()


def test_skill_has_readme(skill: Skill) -> None:
    readme = skill.path / "README.md"
    assert readme.exists(), f"{skill.name}: missing README.md"
    body = readme.read_text(encoding="utf-8").strip()
    assert len(body) > 50, f"{skill.name}: README.md is too short to be useful"


def test_skill_has_changelog(skill: Skill) -> None:
    changelog = skill.path / "CHANGELOG.md"
    assert changelog.exists(), f"{skill.name}: missing CHANGELOG.md"


def test_skill_has_evals(skill: Skill) -> None:
    evals = skill.path / "evals" / "trigger-tests.json"
    assert evals.exists(), f"{skill.name}: missing evals/trigger-tests.json"


def test_skill_has_no_per_skill_plugin_manifest(skill: Skill) -> None:
    """Per-skill ``.claude-plugin/plugin.json`` must NOT exist.

    Claude Code's loader treats a per-skill plugin.json sitting next to the
    SKILL.md as a second component-declaring manifest, conflicting with the
    ``skills: [...]`` entry in marketplace.json. The proven-good pattern
    (``anthropic-agent-skills``) ships zero per-skill plugin.json files;
    marketplace.json is the sole source of truth for plugin metadata.

    If a future skill needs per-skill metadata that the marketplace cannot
    express, restructure to the deep-nested layout
    (``plugins/<plugin>/skills/<skill>/SKILL.md``) so plugin.json sits at
    the plugin root, not inside the skill directory.
    """
    plugin_json = skill.path / ".claude-plugin" / "plugin.json"
    assert not plugin_json.exists(), (
        f"{skill.name}: a per-skill plugin.json exists at {plugin_json}. "
        "Claude Code's /doctor reports this as a conflicting manifest. "
        "Delete it — marketplace.json is authoritative."
    )


def test_skill_body_is_nonempty(skill: Skill) -> None:
    assert len(skill.body.strip()) > 100, (
        f"{skill.name}: SKILL.md body has < 100 chars after frontmatter. "
        "A frontmatter-only skill never gets invoked usefully."
    )


def test_skill_body_has_overview(skill: Skill) -> None:
    # Either "# <name>" or "## Overview" heading is acceptable.
    body_lower = skill.body.lower()
    assert "## overview" in body_lower or "# " in skill.body, (
        f"{skill.name}: SKILL.md body missing any top-level heading or Overview section."
    )


def test_no_hidden_files_in_skill(skill: Skill) -> None:
    """Flag stray hidden files (common cause of install / crawl problems)."""
    stray = [
        p.name
        for p in skill.path.rglob(".*")
        if p.is_file()
        and p.name not in {".gitignore", ".gitkeep"}
        and ".claude-plugin" not in p.parts
    ]
    assert not stray, f"{skill.name}: unexpected hidden files: {stray}"
