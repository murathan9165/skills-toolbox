"""E2E test: defer to Claude Code's own ``claude plugin validate``.

This is the highest-fidelity check available — it uses the real validator
shipped with the Claude Code CLI, the same code path users hit when adding
the marketplace.

The test is skipped when the ``claude`` binary is not on PATH (e.g. on bare
CI runners). When present, it runs the validator on:

* the marketplace root (validates ``.claude-plugin/marketplace.json``)
* every plugin source declared in the marketplace (validates each
  ``.claude-plugin/plugin.json`` in turn)
"""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path
from typing import Any

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
def test_each_plugin_source_passes_official_validator(
    marketplace_manifest: dict[str, Any],
    repo_root: Path,
) -> None:
    """Every plugin source dir that contains a ``.claude-plugin/plugin.json``
    must individually pass ``claude plugin validate``. This catches per-plugin
    schema violations like ``repository: expected string, received object``
    that the marketplace-level validator does not always surface.
    """
    seen_sources: set[Path] = set()
    for plugin in marketplace_manifest["plugins"]:
        source = plugin.get("source")
        if not isinstance(source, str):
            continue
        plugin_dir = (repo_root / source).resolve()
        if plugin_dir in seen_sources:
            continue
        seen_sources.add(plugin_dir)
        if not (plugin_dir / ".claude-plugin" / "plugin.json").is_file():
            # Plugin defined entirely by the marketplace entry (strict: false).
            continue
        proc = subprocess.run(
            [CLAUDE_BIN, "plugin", "validate", str(plugin_dir)],
            capture_output=True,
            text=True,
            timeout=30,
        )
        assert proc.returncode == 0, (
            f"claude plugin validate {plugin_dir} failed:\n"
            f"--- stdout ---\n{proc.stdout}\n--- stderr ---\n{proc.stderr}"
        )


@pytest.mark.skipif(CLAUDE_BIN is None, reason="`claude` CLI not on PATH")
def test_every_skill_plugin_json_passes_official_validator(
    repo_root: Path,
) -> None:
    """Belt-and-braces: every ``skills/*/.claude-plugin/plugin.json`` we ship
    in the repo must validate, even if the marketplace doesn't directly
    consume it. This is the file users see when browsing the repo or
    project-scope-installing a single skill.
    """
    skills_dir = repo_root / "skills"
    if not skills_dir.is_dir():
        pytest.skip("no skills/ directory")
    for plugin_json in skills_dir.glob("*/.claude-plugin/plugin.json"):
        plugin_dir = plugin_json.parent.parent
        # Ensure the JSON itself parses first — give a clearer error than the
        # validator's stack trace if it doesn't.
        json.loads(plugin_json.read_text(encoding="utf-8"))
        proc = subprocess.run(
            [CLAUDE_BIN, "plugin", "validate", str(plugin_dir)],
            capture_output=True,
            text=True,
            timeout=30,
        )
        assert proc.returncode == 0, (
            f"claude plugin validate {plugin_dir} failed:\n"
            f"--- stdout ---\n{proc.stdout}\n--- stderr ---\n{proc.stderr}"
        )
