"""E2E: trigger-tests.json is well-formed and covers should / shouldn't cases.

This is a *structural* check. A live-LLM accuracy check lives under ``tests/live/``
and is excluded from default CI (requires an API key).
"""

from __future__ import annotations

import json

import pytest

from tests.conftest import Skill

MIN_CASES = 20
MIN_POLARITY_SHARE = 0.30  # at least 30% of each polarity


def _load_eval_cases(skill: Skill) -> list[dict]:
    path = skill.path / "evals" / "trigger-tests.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    assert "cases" in data, f"{skill.name}: evals/trigger-tests.json missing 'cases'"
    return data["cases"]


def test_eval_case_count(skill: Skill) -> None:
    cases = _load_eval_cases(skill)
    assert len(cases) >= MIN_CASES, (
        f"{skill.name}: trigger-tests.json has {len(cases)} cases; need ≥ {MIN_CASES}."
    )


def test_eval_case_shape(skill: Skill) -> None:
    cases = _load_eval_cases(skill)
    for case in cases:
        assert isinstance(case, dict)
        for field in ("id", "query", "should_trigger"):
            assert field in case, (
                f"{skill.name}: case {case.get('id', '<unnamed>')} missing '{field}'"
            )
        assert isinstance(case["query"], str) and case["query"].strip()
        assert isinstance(case["should_trigger"], bool)


def test_eval_case_id_uniqueness(skill: Skill) -> None:
    cases = _load_eval_cases(skill)
    ids = [c["id"] for c in cases]
    duplicates = {i for i in ids if ids.count(i) > 1}
    assert not duplicates, f"{skill.name}: duplicate case ids: {duplicates}"


def test_eval_polarity_balance(skill: Skill) -> None:
    cases = _load_eval_cases(skill)
    total = len(cases)
    positives = sum(1 for c in cases if c["should_trigger"])
    negatives = total - positives
    pos_share = positives / total
    neg_share = negatives / total
    assert pos_share >= MIN_POLARITY_SHARE, (
        f"{skill.name}: only {positives}/{total} positive cases "
        f"({pos_share:.0%}); need ≥ {MIN_POLARITY_SHARE:.0%}."
    )
    assert neg_share >= MIN_POLARITY_SHARE, (
        f"{skill.name}: only {negatives}/{total} negative cases "
        f"({neg_share:.0%}); need ≥ {MIN_POLARITY_SHARE:.0%}."
    )


def test_eval_cases_have_rationale(skill: Skill) -> None:
    cases = _load_eval_cases(skill)
    missing = [c["id"] for c in cases if not c.get("rationale")]
    # Rationale is strongly encouraged but not strictly required — warn via skip
    # when entirely absent.
    if len(missing) == len(cases):
        pytest.skip(f"{skill.name}: no rationales declared; consider adding.")
    assert len(missing) < len(cases) * 0.5, (
        f"{skill.name}: {len(missing)} of {len(cases)} cases lack rationale. "
        "Rationales make description-tuning decisions traceable."
    )
