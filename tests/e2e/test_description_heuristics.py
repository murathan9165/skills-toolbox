"""E2E: SKILL.md descriptions follow superpowers:writing-skills heuristics.

These are *heuristic* rules that have outsized impact on trigger accuracy.
Every skill description should:
- Start with "Use when ..." (triggering-only).
- Be written in third person (no "I " / "we " / "our ").
- Contain at least 4 distinct trigger phrases / vocabulary terms.
- Avoid summarising the skill's process or workflow.
- Stay within the 1024-character spec cap (also enforced in unit tests).
"""

from __future__ import annotations

import re

from tests.conftest import Skill

FIRST_PERSON_RE = re.compile(r"\b(I|I'm|I'll|I've|we|we're|our|us|my)\b", re.IGNORECASE)

# A rough proxy for "vocabulary spread": count quoted trigger phrases and
# comma-separated trigger keywords. Require ≥ 4 across the description.
TRIGGER_PHRASE_RE = re.compile(r'"([^"]{2,60})"')
COMMA_TOKEN_RE = re.compile(r"([a-z][a-z\- ]{2,30})\s*[,.;]", re.IGNORECASE)


def test_description_starts_with_use_when(skill: Skill) -> None:
    desc: str = skill.frontmatter["description"].strip()
    assert desc.lower().startswith("use when"), (
        f"{skill.name}: description should start with 'Use when ...'. Got: {desc[:40]!r}"
    )


def test_description_is_third_person(skill: Skill) -> None:
    desc: str = skill.frontmatter["description"]
    hits = FIRST_PERSON_RE.findall(desc)
    # Allow "we" inside quoted trigger phrases like "what should we build"
    hits_unquoted = [h for h in hits if not any(h in q for q in TRIGGER_PHRASE_RE.findall(desc))]
    assert not hits_unquoted, (
        f"{skill.name}: description contains first-person tokens {hits_unquoted} "
        "outside of quoted trigger phrases. Descriptions must be third person."
    )


def test_description_has_vocabulary_spread(skill: Skill) -> None:
    desc: str = skill.frontmatter["description"]
    trigger_phrases = TRIGGER_PHRASE_RE.findall(desc)
    tokens = COMMA_TOKEN_RE.findall(desc)
    total = len(trigger_phrases) + len(tokens)
    assert total >= 4, (
        f"{skill.name}: description has only {total} distinct trigger phrases / "
        "vocabulary tokens; need ≥ 4 for cross-persona coverage."
    )


def test_description_length_under_cap(skill: Skill) -> None:
    desc: str = skill.frontmatter["description"]
    assert len(desc) <= 1024, f"{skill.name}: description {len(desc)} > 1024 chars (spec cap)."


def test_description_does_not_summarise_workflow(skill: Skill) -> None:
    """Counterpart to the unit test, kept here to reinforce the rule at e2e layer."""
    desc_lower: str = skill.frontmatter["description"].lower()
    forbidden = ("guides the agent", "this skill helps", "this skill provides")
    offenders = [p for p in forbidden if p in desc_lower]
    assert not offenders, (
        f"{skill.name}: description summarises workflow ({offenders}). Descriptions "
        "must describe triggering conditions only."
    )
