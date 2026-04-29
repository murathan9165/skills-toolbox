"""Unit tests: per-skill ``.claude-plugin/plugin.json`` conforms to expected shape."""

from __future__ import annotations

import re

import pytest

from tests.conftest import Skill

SEMVER_RE = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$"
)


def test_plugin_manifest_parses(skill: Skill) -> None:
    assert skill.plugin_manifest is not None, f"{skill.name}: plugin.json did not parse as JSON"
    assert isinstance(skill.plugin_manifest, dict)


@pytest.mark.parametrize("field", ["name", "version", "description"])
def test_plugin_manifest_required_fields(skill: Skill, field: str) -> None:
    assert skill.plugin_manifest is not None
    assert field in skill.plugin_manifest, (
        f"{skill.name}: plugin.json missing required field '{field}'"
    )
    value = skill.plugin_manifest[field]
    assert isinstance(value, str) and value.strip(), (
        f"{skill.name}: plugin.json field '{field}' is empty"
    )


def test_plugin_manifest_version_is_semver(skill: Skill) -> None:
    assert skill.plugin_manifest is not None
    version = skill.plugin_manifest.get("version", "")
    assert SEMVER_RE.match(version), (
        f"{skill.name}: plugin.json version '{version}' is not valid semver."
    )


def test_plugin_manifest_name_matches_skill(skill: Skill) -> None:
    assert skill.plugin_manifest is not None
    assert skill.plugin_manifest["name"] == skill.name, (
        f"{skill.name}: plugin.json name '{skill.plugin_manifest['name']}' "
        f"does not match skill directory '{skill.name}'"
    )


def test_plugin_manifest_repository_is_string(skill: Skill) -> None:
    """Claude Code's plugin.json schema requires ``repository`` to be a string
    URL, not an object. Declaring it as ``{type, url, directory}`` (npm-style)
    fails ``claude plugin validate`` with:

        repository: Invalid input: expected string, received object
    """
    assert skill.plugin_manifest is not None
    repo = skill.plugin_manifest.get("repository")
    if repo is None:
        pytest.skip("repository not declared")
    assert isinstance(repo, str) and repo.strip(), (
        f"{skill.name}: plugin.json 'repository' must be a string URL "
        f"(got {type(repo).__name__}). The npm-style "
        "{type, url, directory} object form fails Claude Code's validator."
    )


def test_plugin_manifest_author_shape(skill: Skill) -> None:
    """``author`` may be a string or an object with at least ``name``."""
    assert skill.plugin_manifest is not None
    author = skill.plugin_manifest.get("author")
    if author is None:
        pytest.skip("author not declared")
    if isinstance(author, str):
        assert author.strip(), f"{skill.name}: plugin.json author string is empty"
        return
    assert isinstance(author, dict), f"{skill.name}: plugin.json author must be string or object"
    assert author.get("name"), f"{skill.name}: plugin.json author object must include 'name'"


def test_plugin_manifest_keywords_are_list(skill: Skill) -> None:
    assert skill.plugin_manifest is not None
    keywords = skill.plugin_manifest.get("keywords")
    if keywords is None:
        pytest.skip("keywords not declared")
    assert isinstance(keywords, list)
    assert all(isinstance(k, str) and k for k in keywords), (
        f"{skill.name}: plugin.json keywords must be a list of non-empty strings"
    )
    assert len(keywords) >= 3, (
        f"{skill.name}: plugin.json should declare ≥ 3 keywords for registry search."
    )
