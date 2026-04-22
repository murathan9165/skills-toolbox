"""Integration tests: name/version consistency across all manifests.

SKILL.md frontmatter is the single source of truth. plugin.json, marketplace.json,
and skills.json entries must agree.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from tests.conftest import Skill


def test_frontmatter_matches_plugin_manifest_identity(skill: Skill) -> None:
    """name and version are identity fields; they must match exactly.

    description is intentionally allowed to differ: SKILL.md description is the
    trigger signal injected into agent prompts (verbose, keyword-rich), while
    plugin.json description is the marketing blurb that shows in registries.
    """
    assert skill.plugin_manifest is not None
    for field in ("name", "version"):
        fm = skill.frontmatter.get(field)
        pj = skill.plugin_manifest.get(field)
        assert fm == pj, (
            f"{skill.name}: SKILL.md frontmatter '{field}' ({fm!r}) does not match "
            f"plugin.json '{field}' ({pj!r})"
        )


def test_plugin_manifest_description_is_nonempty(skill: Skill) -> None:
    """plugin.json description can differ from SKILL.md description but must exist
    and be reasonably short (< 400 chars — registry card length)."""
    assert skill.plugin_manifest is not None
    desc = skill.plugin_manifest.get("description", "")
    assert desc, f"{skill.name}: plugin.json description is empty"
    assert len(desc) < 400, (
        f"{skill.name}: plugin.json description is {len(desc)} chars; "
        "keep it under 400 so it fits on registry cards."
    )


def test_marketplace_lists_every_skill(
    marketplace_manifest: dict[str, Any],
    skills: list[Skill],
    repo_root: Path,
) -> None:
    market_sources = {
        (repo_root / p["source"]).resolve() for p in marketplace_manifest["plugins"]
    }
    for s in skills:
        assert s.path.resolve() in market_sources, (
            f"Skill {s.name} at {s.path} is not listed in marketplace.json"
        )


def test_skills_manifest_lists_every_skill(
    skills_manifest: dict[str, Any],
    skills: list[Skill],
    repo_root: Path,
) -> None:
    manifest_paths = {
        (repo_root / entry["path"]).resolve()
        for entry in skills_manifest["skills"]
    }
    for s in skills:
        assert s.path.resolve() in manifest_paths, (
            f"Skill {s.name} at {s.path} is not listed in skills.json"
        )


def test_marketplace_and_skills_manifest_agree_on_names(
    marketplace_manifest: dict[str, Any],
    skills_manifest: dict[str, Any],
) -> None:
    market = {p["name"] for p in marketplace_manifest["plugins"]}
    sh = {e["name"] for e in skills_manifest["skills"]}
    assert market == sh, (
        f"marketplace.json plugins {market} and skills.json skills {sh} do not agree."
    )
