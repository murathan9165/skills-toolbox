"""E2E test: defer to Claude Code's own ``claude plugin validate``.

This is the highest-fidelity check available — it uses the real validator
shipped with the Claude Code CLI, the same code path users hit when adding
the marketplace.

The test is skipped when the ``claude`` binary is not on PATH (e.g. on bare
CI runners). When present, it runs the validator on the marketplace root
(``.claude-plugin/marketplace.json``).

Per-skill ``plugin.json`` was removed because Claude Code's loader treats
it as a conflicting component-declaring manifest (reported by
``/doctor``). marketplace.json is now the sole plugin manifest.
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pytest

CLAUDE_BIN = shutil.which("claude")


@pytest.mark.skipif(CLAUDE_BIN is None, reason="`claude` CLI not on PATH")
def test_marketplace_passes_official_validator(repo_root: Path) -> None:
    proc = subprocess.run(
        [CLAUDE_BIN, "plugin", "validate", "."],
        cwd=repo_root,
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert proc.returncode == 0, (
        "claude plugin validate . failed:\n"
        f"--- stdout ---\n{proc.stdout}\n--- stderr ---\n{proc.stderr}"
    )


@pytest.mark.skipif(CLAUDE_BIN is None, reason="`claude` CLI not on PATH")
def test_no_per_skill_plugin_json_files_remain(repo_root: Path) -> None:
    """Hard rule: no per-skill ``.claude-plugin/plugin.json`` may exist anywhere
    under ``skills/``. Their presence triggers the conflicting-manifests error
    in ``claude /doctor`` (see ``test_strict_false_skills_paths_have_no_sibling_plugin_json``).
    """
    skills_dir = repo_root / "skills"
    if not skills_dir.is_dir():
        pytest.skip("no skills/ directory")
    offenders = sorted(
        p.relative_to(repo_root) for p in skills_dir.rglob(".claude-plugin/plugin.json")
    )
    assert not offenders, (
        f"Found per-skill plugin.json files: {offenders}. "
        "Delete them — marketplace.json is the sole source of plugin metadata."
    )
