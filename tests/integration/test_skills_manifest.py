"""Integration tests: repo-level ``skills.json`` (skills.sh bundle) is sane."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+")


def test_skills_manifest_top_level_fields(skills_manifest: dict[str, Any]) -> None:
    for field in ("name", "version", "description", "skills"):
        assert field in skills_manifest, f"skills.json missing '{field}'"


def test_skills_manifest_version_is_semver(skills_manifest: dict[str, Any]) -> None:
    version = skills_manifest["version"]
    assert SEMVER_RE.match(version), (
        f"skills.json version '{version}' is not semver-like."
    )


def test_skills_manifest_skills_is_nonempty_list(
    skills_manifest: dict[str, Any],
) -> None:
    assert isinstance(skills_manifest["skills"], list)
    assert skills_manifest["skills"], "skills.json declares no skills"


def test_every_skills_entry_has_required_fields(
    skills_manifest: dict[str, Any],
) -> None:
    required = {"name", "path", "description"}
    for entry in skills_manifest["skills"]:
        missing = required - entry.keys()
        assert not missing, (
            f"skills.json entry {entry.get('name', '<unnamed>')} missing: {missing}"
        )


def test_every_skills_entry_path_exists(
    skills_manifest: dict[str, Any],
    repo_root: Path,
) -> None:
    for entry in skills_manifest["skills"]:
        path = repo_root / entry["path"]
        assert path.exists(), (
            f"skills.json entry {entry['name']}: path {entry['path']!r} missing"
        )
        assert (path / "SKILL.md").exists(), (
            f"skills.json entry {entry['name']}: {entry['path']!r} lacks SKILL.md"
        )
