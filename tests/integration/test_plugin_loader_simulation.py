"""Integration test: simulate Claude Code's plugin loader.

This test resolves each plugin entry in ``.claude-plugin/marketplace.json``
the way Claude Code's loader does and asserts the SKILL.md is reachable.

Per the Claude Code marketplace docs
(https://code.claude.com/docs/en/plugin-marketplaces):

* A plugin's ``source`` is copied into the user's plugin cache.
* Skills are discovered at ``<source>/skills/<name>/SKILL.md`` by default.
* The ``skills`` field on the plugin entry overrides the default. Each entry
  is a path (relative to ``source``) to a directory that itself contains
  ``SKILL.md`` (matching the empirical layout of ``anthropic-agent-skills``).
* When ``strict`` is ``false``, the marketplace entry alone defines components
  and a per-plugin ``plugin.json`` declaring components is not required (and
  may not declare conflicting components).

If this test fails, end users will see "plugin installs but skill never
loads" — the exact bug this regression test exists to prevent.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any


def _resolve_skill_md_paths(plugin: dict[str, Any], repo_root: Path) -> list[Path]:
    """Return every SKILL.md path Claude Code would load for this plugin entry."""
    source = plugin["source"]
    if not isinstance(source, str):
        # Object sources (github/url/git-subdir/npm) are not used by this repo;
        # if they ever are, the test author should extend this resolver.
        raise AssertionError(
            f"plugin {plugin.get('name')!r} uses a non-string source "
            f"({source!r}); extend the loader simulation to handle it."
        )
    plugin_root = (repo_root / source).resolve()

    skills_field = plugin.get("skills")
    paths: list[Path] = []

    if skills_field is None:
        # Default discovery: <plugin_root>/skills/<name>/SKILL.md for every
        # subdirectory of <plugin_root>/skills/ that contains a SKILL.md.
        default_dir = plugin_root / "skills"
        if default_dir.is_dir():
            for child in sorted(default_dir.iterdir()):
                if child.is_dir() and (child / "SKILL.md").is_file():
                    paths.append(child / "SKILL.md")
        return paths

    if isinstance(skills_field, str):
        skills_field = [skills_field]
    if not isinstance(skills_field, list):
        raise AssertionError(
            f"plugin {plugin.get('name')!r} 'skills' must be a string or list, "
            f"got {type(skills_field).__name__}"
        )

    for entry in skills_field:
        # Empirically (anthropic-agent-skills marketplace.json), each entry
        # points directly to a directory containing SKILL.md.
        candidate = (plugin_root / entry).resolve()
        paths.append(candidate / "SKILL.md")
    return paths


def test_every_marketplace_plugin_resolves_to_at_least_one_skill_md(
    marketplace_manifest: dict[str, Any],
    repo_root: Path,
) -> None:
    """Each plugin entry must yield at least one loadable SKILL.md."""
    for plugin in marketplace_manifest["plugins"]:
        paths = _resolve_skill_md_paths(plugin, repo_root)
        assert paths, (
            f"marketplace plugin {plugin['name']!r}: loader resolved zero "
            "SKILL.md files. Either add 'skills': [...] to the plugin entry or "
            "place SKILL.md at <source>/skills/<name>/SKILL.md."
        )


def test_every_resolved_skill_md_exists(
    marketplace_manifest: dict[str, Any],
    repo_root: Path,
) -> None:
    """Every SKILL.md the loader would try to read must actually exist."""
    for plugin in marketplace_manifest["plugins"]:
        for skill_md in _resolve_skill_md_paths(plugin, repo_root):
            assert skill_md.is_file(), (
                f"marketplace plugin {plugin['name']!r}: loader expects "
                f"{skill_md.relative_to(repo_root)} but it does not exist."
            )


def test_strict_false_plugins_have_no_conflicting_plugin_json(
    marketplace_manifest: dict[str, Any],
    repo_root: Path,
) -> None:
    """When ``strict: false`` the marketplace is authoritative; any per-plugin
    ``plugin.json`` at the source root must NOT declare components or the
    plugin fails to load (per docs).
    """
    component_keys = {"skills", "commands", "agents", "hooks", "mcpServers", "lspServers"}
    import json

    for plugin in marketplace_manifest["plugins"]:
        if plugin.get("strict", True):
            continue  # default-strict plugins use plugin.json freely
        source = plugin["source"]
        if not isinstance(source, str):
            continue
        manifest_path = (repo_root / source).resolve() / ".claude-plugin" / "plugin.json"
        if not manifest_path.is_file():
            continue
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        conflicting = component_keys & manifest.keys()
        assert not conflicting, (
            f"marketplace plugin {plugin['name']!r}: strict=false but "
            f"{manifest_path.relative_to(repo_root)} declares "
            f"{sorted(conflicting)} — this is a documented load failure."
        )


def test_marketplace_plugins_have_version_field(
    marketplace_manifest: dict[str, Any],
) -> None:
    """Pinning is required for stable updates; version must live in the plugin
    entry or in plugin.json. We require it on the marketplace entry to keep
    publishing-side discipline visible.
    """
    for plugin in marketplace_manifest["plugins"]:
        assert plugin.get("version"), (
            f"marketplace plugin {plugin['name']!r}: missing 'version'. "
            "Without it Claude Code falls back to the commit SHA and updates "
            "are opaque to users."
        )
