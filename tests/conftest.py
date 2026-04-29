"""Shared pytest fixtures for skills-toolbox tests.

Discovers every skill under ``skills/`` and exposes parsed SKILL.md frontmatter,
SKILL.md body, and the per-skill plugin manifest. Also exposes the repo-level
``marketplace.json``, ``skills.json``, and ``README.md``.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / "skills"

FRONTMATTER_RE = re.compile(
    r"\A---\s*\n(?P<frontmatter>.*?)\n---\s*\n(?P<body>.*)",
    re.DOTALL,
)


@dataclass(frozen=True)
class Skill:
    """Parsed view of a single skill directory."""

    name: str
    path: Path
    skill_md_path: Path
    frontmatter: dict[str, Any]
    body: str
    plugin_manifest_path: Path | None
    plugin_manifest: dict[str, Any] | None


def _parse_skill_md(skill_md: Path) -> tuple[dict[str, Any], str]:
    text = skill_md.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(text)
    if match is None:
        raise ValueError(f"{skill_md} does not start with a YAML frontmatter block (--- ... ---).")
    frontmatter = yaml.safe_load(match.group("frontmatter")) or {}
    if not isinstance(frontmatter, dict):
        raise ValueError(f"{skill_md} frontmatter did not parse as a YAML mapping.")
    return frontmatter, match.group("body")


def _load_skill(skill_dir: Path) -> Skill:
    skill_md = skill_dir / "SKILL.md"
    frontmatter, body = _parse_skill_md(skill_md)

    plugin_manifest_path = skill_dir / ".claude-plugin" / "plugin.json"
    plugin_manifest: dict[str, Any] | None = None
    if plugin_manifest_path.exists():
        plugin_manifest = json.loads(plugin_manifest_path.read_text(encoding="utf-8"))

    return Skill(
        name=skill_dir.name,
        path=skill_dir,
        skill_md_path=skill_md,
        frontmatter=frontmatter,
        body=body,
        plugin_manifest_path=plugin_manifest_path if plugin_manifest is not None else None,
        plugin_manifest=plugin_manifest,
    )


def _discover_skills() -> list[Skill]:
    if not SKILLS_DIR.is_dir():
        return []
    skills: list[Skill] = []
    for entry in sorted(SKILLS_DIR.iterdir()):
        if not entry.is_dir():
            continue
        if (entry / "SKILL.md").exists():
            skills.append(_load_skill(entry))
    return skills


# --- Fixtures ----------------------------------------------------------------


@pytest.fixture(scope="session")
def repo_root() -> Path:
    return REPO_ROOT


@pytest.fixture(scope="session")
def skills() -> list[Skill]:
    """Every discovered skill in the repo."""
    return _discover_skills()


@pytest.fixture(scope="session")
def marketplace_manifest(repo_root: Path) -> dict[str, Any]:
    path = repo_root / ".claude-plugin" / "marketplace.json"
    assert path.exists(), f"Missing {path} — every toolbox repo must have marketplace.json"
    return json.loads(path.read_text(encoding="utf-8"))


@pytest.fixture(scope="session")
def skills_manifest(repo_root: Path) -> dict[str, Any]:
    path = repo_root / "skills.json"
    assert path.exists(), f"Missing {path} — every toolbox repo must have skills.json"
    return json.loads(path.read_text(encoding="utf-8"))


@pytest.fixture(scope="session")
def readme_text(repo_root: Path) -> str:
    path = repo_root / "README.md"
    assert path.exists(), f"Missing {path} — every toolbox repo must have a README.md"
    return path.read_text(encoding="utf-8")


def pytest_generate_tests(metafunc: pytest.Metafunc) -> None:
    """Parametrize any test taking a ``skill`` fixture with each discovered skill."""
    if "skill" in metafunc.fixturenames:
        discovered = _discover_skills()
        metafunc.parametrize(
            "skill",
            discovered,
            ids=[s.name for s in discovered],
        )
