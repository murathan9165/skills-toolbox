"""E2E: every skill on disk is reachable from the top-level README catalog."""

from __future__ import annotations

from tests.conftest import Skill


def test_readme_mentions_every_skill(skills: list[Skill], readme_text: str) -> None:
    for s in skills:
        assert s.name in readme_text, (
            f"Top-level README.md does not mention skill {s.name!r}. Every skill "
            "must appear in the catalog so humans browsing GitHub can find it."
        )


def test_readme_has_install_instructions(readme_text: str) -> None:
    for marker in ("claude plugin marketplace add", "skills-toolbox"):
        assert marker in readme_text, f"README.md missing install instruction marker: {marker!r}"


def test_readme_references_license(readme_text: str) -> None:
    assert "License" in readme_text or "license" in readme_text, (
        "README.md must mention the license."
    )
