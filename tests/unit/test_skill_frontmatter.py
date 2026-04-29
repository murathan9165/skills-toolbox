"""Unit tests: SKILL.md frontmatter conforms to the Agent Skills spec.

Rules enforced:
- ``name`` is present and matches ``^[a-z][a-z0-9-]{1,63}$`` (lowercase, hyphens).
- ``description`` is present, non-empty, and ≤ 1024 characters.
- ``description`` contains no XML tags (per spec).
- ``description`` does not start with "Guides" or similar workflow-summary patterns.
- ``version`` if present is valid semver.
"""

from __future__ import annotations

import re

import pytest

from tests.conftest import Skill

NAME_RE = re.compile(r"^[a-z][a-z0-9-]{1,63}$")
SEMVER_RE = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$"
)
DESCRIPTION_MAX_LEN = 1024

# Description must be triggering, not workflow summary. See writing-skills guidance.
WORKFLOW_SUMMARY_PATTERNS = (
    "guides the agent",
    "this skill helps",
    "this skill provides",
    "this skill will",
    "the skill will",
)


def test_frontmatter_is_a_mapping(skill: Skill) -> None:
    assert isinstance(skill.frontmatter, dict)
    assert skill.frontmatter, f"{skill.skill_md_path} has empty frontmatter."


def test_name_present_and_valid(skill: Skill) -> None:
    name = skill.frontmatter.get("name")
    assert name, f"{skill.skill_md_path} is missing required field 'name'"
    assert isinstance(name, str)
    assert NAME_RE.match(name), (
        f"name '{name}' in {skill.skill_md_path} violates "
        "^[a-z][a-z0-9-]{1,63}$ (lowercase, starts with letter, hyphens allowed)."
    )


def test_name_matches_directory(skill: Skill) -> None:
    assert skill.frontmatter["name"] == skill.path.name, (
        f"SKILL.md name '{skill.frontmatter['name']}' does not match "
        f"directory name '{skill.path.name}'"
    )


def test_description_present(skill: Skill) -> None:
    desc = skill.frontmatter.get("description")
    assert desc, f"{skill.skill_md_path} is missing required field 'description'"
    assert isinstance(desc, str)
    assert desc.strip(), "description is empty / whitespace-only"


def test_description_length(skill: Skill) -> None:
    desc: str = skill.frontmatter["description"]
    assert len(desc) <= DESCRIPTION_MAX_LEN, (
        f"description for {skill.name} is {len(desc)} chars (spec cap: {DESCRIPTION_MAX_LEN})."
    )


def test_description_no_xml_tags(skill: Skill) -> None:
    desc: str = skill.frontmatter["description"]
    assert not re.search(r"<[a-zA-Z][^>]*>", desc), (
        f"description for {skill.name} contains XML tags; spec forbids them."
    )


def test_description_is_triggering_not_summary(skill: Skill) -> None:
    desc_lower: str = skill.frontmatter["description"].lower()
    offenders = [p for p in WORKFLOW_SUMMARY_PATTERNS if p in desc_lower]
    assert not offenders, (
        f"description for {skill.name} contains workflow-summary phrase(s) {offenders}. "
        "Descriptions should describe WHEN to trigger, not WHAT the skill does — see "
        "superpowers:writing-skills."
    )


def test_description_starts_with_use_when(skill: Skill) -> None:
    desc: str = skill.frontmatter["description"].strip().lower()
    assert desc.startswith("use when"), (
        f"description for {skill.name} should start with 'Use when ...' to focus "
        f"on triggering conditions. Got: {desc[:40]!r}"
    )


@pytest.mark.parametrize("field", ["version", "author", "license"])
def test_recommended_fields_present(skill: Skill, field: str) -> None:
    assert field in skill.frontmatter, (
        f"{skill.name}: recommended frontmatter field '{field}' is missing."
    )


def test_version_is_valid_semver(skill: Skill) -> None:
    version = skill.frontmatter.get("version")
    if version is None:
        pytest.skip("version not declared")
    assert SEMVER_RE.match(str(version)), f"{skill.name}: version '{version}' is not valid semver."
