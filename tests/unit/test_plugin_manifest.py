"""Unit tests: each skill's marketplace plugin entry conforms to expected shape.

Per-skill ``.claude-plugin/plugin.json`` was removed: Claude Code's loader
reports a conflicting-manifests error in ``/doctor`` when a plugin.json sits
inside a skill directory that the marketplace also declares via
``skills: [...]``. ``marketplace.json`` is now authoritative; these tests
validate the marketplace plugin entry that corresponds to each discovered
skill.
"""

from __future__ import annotations

import re
from typing import Any

import pytest

from tests.conftest import Skill

SEMVER_RE = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$"
)


def _entry_for(skill: Skill, by_name: dict[str, dict[str, Any]]) -> dict[str, Any]:
    entry = by_name.get(skill.name)
    assert entry is not None, (
        f"{skill.name}: no marketplace.json plugin entry. Add the skill to "
        ".claude-plugin/marketplace.json plugins[]."
    )
    return entry


@pytest.mark.parametrize("field", ["name", "version", "description"])
def test_marketplace_entry_required_fields(
    skill: Skill,
    marketplace_plugin_by_name: dict[str, dict[str, Any]],
    field: str,
) -> None:
    entry = _entry_for(skill, marketplace_plugin_by_name)
    value = entry.get(field)
    assert isinstance(value, str) and value.strip(), (
        f"{skill.name}: marketplace entry missing or empty '{field}'"
    )


def test_marketplace_entry_version_is_semver(
    skill: Skill,
    marketplace_plugin_by_name: dict[str, dict[str, Any]],
) -> None:
    entry = _entry_for(skill, marketplace_plugin_by_name)
    version = entry.get("version", "")
    assert SEMVER_RE.match(version), (
        f"{skill.name}: marketplace entry version '{version}' is not valid semver."
    )


def test_marketplace_entry_name_matches_skill(
    skill: Skill,
    marketplace_plugin_by_name: dict[str, dict[str, Any]],
) -> None:
    entry = _entry_for(skill, marketplace_plugin_by_name)
    assert entry["name"] == skill.name, (
        f"{skill.name}: marketplace entry name '{entry['name']}' does not match skill directory."
    )


def test_marketplace_entry_keywords_are_list(
    skill: Skill,
    marketplace_plugin_by_name: dict[str, dict[str, Any]],
) -> None:
    entry = _entry_for(skill, marketplace_plugin_by_name)
    keywords = entry.get("keywords")
    if keywords is None:
        pytest.skip("keywords not declared")
    assert isinstance(keywords, list)
    assert all(isinstance(k, str) and k for k in keywords), (
        f"{skill.name}: marketplace entry keywords must be a list of non-empty strings"
    )
    assert len(keywords) >= 3, (
        f"{skill.name}: marketplace entry should declare ≥ 3 keywords for registry search."
    )


def test_marketplace_entry_author_shape(
    skill: Skill,
    marketplace_plugin_by_name: dict[str, dict[str, Any]],
) -> None:
    """``author`` may be a string or an object with at least ``name``."""
    entry = _entry_for(skill, marketplace_plugin_by_name)
    author = entry.get("author")
    if author is None:
        pytest.skip("author not declared")
    if isinstance(author, str):
        assert author.strip(), f"{skill.name}: marketplace entry author string is empty"
        return
    assert isinstance(author, dict), (
        f"{skill.name}: marketplace entry author must be string or object"
    )
    assert author.get("name"), f"{skill.name}: marketplace entry author object must include 'name'"


def test_marketplace_entry_repository_is_string_if_present(
    skill: Skill,
    marketplace_plugin_by_name: dict[str, dict[str, Any]],
) -> None:
    """Claude Code's plugin schema requires ``repository`` to be a string URL,
    not the npm-style ``{type, url, directory}`` object."""
    entry = _entry_for(skill, marketplace_plugin_by_name)
    repo = entry.get("repository")
    if repo is None:
        pytest.skip("repository not declared")
    assert isinstance(repo, str) and repo.strip(), (
        f"{skill.name}: marketplace entry 'repository' must be a string URL "
        f"(got {type(repo).__name__})."
    )
