"""Integration tests: name/version consistency across all manifests.

SKILL.md frontmatter is the single source of truth for skill identity.
The marketplace.json plugin entry (which doubles as plugin metadata, since
per-skill plugin.json was removed) and skills.json must agree.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from tests.conftest import Skill


def test_frontmatter_matches_marketplace_entry_identity(
    skill: Skill,
    marketplace_plugin_by_name: dict[str, dict[str, Any]],
) -> None:
    """name and version are identity fields; they must match exactly between
    SKILL.md frontmatter and the marketplace plugin entry.

    description is intentionally allowed to differ: SKILL.md description is the
    trigger signal injected into agent prompts (verbose, keyword-rich), while
    the marketplace description is the marketing blurb on registry cards.
    """
    entry = marketplace_plugin_by_name.get(skill.name)
    assert entry is not None, f"{skill.name}: missing from marketplace.json plugins[]"
    for field in ("name", "version"):
        fm = skill.frontmatter.get(field)
        me = entry.get(field)
        assert fm == me, (
            f"{skill.name}: SKILL.md frontmatter '{field}' ({fm!r}) does not match "
            f"marketplace entry '{field}' ({me!r})"
        )


def test_marketplace_entry_description_is_nonempty(
    skill: Skill,
    marketplace_plugin_by_name: dict[str, dict[str, Any]],
) -> None:
    """Marketplace description can differ from SKILL.md description but must
    exist and be reasonably short (< 400 chars — registry card length)."""
    entry = marketplace_plugin_by_name.get(skill.name)
    assert entry is not None
    desc = entry.get("description", "")
    assert desc, f"{skill.name}: marketplace entry description is empty"
    assert len(desc) < 400, (
        f"{skill.name}: marketplace entry description is {len(desc)} chars; "
        "keep it under 400 so it fits on registry cards."
    )


def test_marketplace_lists_every_skill(
    marketplace_manifest: dict[str, Any],
    skills: list[Skill],
    repo_root: Path,
) -> None:
    """Every discovered skill directory must be reachable from at least one
    marketplace plugin entry — either as the plugin's ``source`` (legacy
    pattern) or as one of its ``skills`` paths (canonical pattern).
    """
    reachable: set[Path] = set()
    for plugin in marketplace_manifest["plugins"]:
        source = plugin.get("source")
        if not isinstance(source, str):
            continue
        plugin_root = (repo_root / source).resolve()
        skills_field = plugin.get("skills")
        if skills_field is None:
            # Default discovery dir
            default = plugin_root / "skills"
            if default.is_dir():
                for child in default.iterdir():
                    if child.is_dir() and (child / "SKILL.md").is_file():
                        reachable.add(child.resolve())
            # Some toolboxes also expose the plugin root itself as a skill dir
            if (plugin_root / "SKILL.md").is_file():
                reachable.add(plugin_root)
            continue
        if isinstance(skills_field, str):
            skills_field = [skills_field]
        for entry in skills_field:
            reachable.add((plugin_root / entry).resolve())

    for s in skills:
        assert s.path.resolve() in reachable, (
            f"Skill {s.name} at {s.path} is not reachable from any "
            "marketplace.json plugin entry (checked source defaults and "
            "explicit 'skills' arrays)."
        )


def test_skills_manifest_lists_every_skill(
    skills_manifest: dict[str, Any],
    skills: list[Skill],
    repo_root: Path,
) -> None:
    manifest_paths = {(repo_root / entry["path"]).resolve() for entry in skills_manifest["skills"]}
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
