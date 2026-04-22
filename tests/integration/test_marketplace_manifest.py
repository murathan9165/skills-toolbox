"""Integration tests: repo-level ``.claude-plugin/marketplace.json`` is sane."""

from __future__ import annotations

from pathlib import Path
from typing import Any


def test_marketplace_has_name_and_owner(marketplace_manifest: dict[str, Any]) -> None:
    assert marketplace_manifest.get("name"), "marketplace.json missing 'name'"
    owner = marketplace_manifest.get("owner")
    assert isinstance(owner, dict) and owner.get("name"), (
        "marketplace.json missing owner.name"
    )


def test_marketplace_has_plugins_list(marketplace_manifest: dict[str, Any]) -> None:
    plugins = marketplace_manifest.get("plugins")
    assert isinstance(plugins, list), "marketplace.json 'plugins' must be a list"
    assert plugins, "marketplace.json 'plugins' is empty — nothing to publish."


def test_every_marketplace_plugin_has_required_fields(
    marketplace_manifest: dict[str, Any],
) -> None:
    required = {"name", "source", "description"}
    for plugin in marketplace_manifest["plugins"]:
        missing = required - plugin.keys()
        assert not missing, (
            f"marketplace plugin {plugin.get('name', '<unnamed>')} missing: {missing}"
        )


def test_every_marketplace_plugin_source_exists(
    marketplace_manifest: dict[str, Any],
    repo_root: Path,
) -> None:
    for plugin in marketplace_manifest["plugins"]:
        source = plugin["source"]
        resolved = (repo_root / source).resolve()
        assert resolved.exists(), (
            f"marketplace plugin {plugin['name']}: source path "
            f"{source!r} does not resolve ({resolved})"
        )
        assert (resolved / "SKILL.md").exists(), (
            f"marketplace plugin {plugin['name']}: source {source!r} "
            "does not contain SKILL.md"
        )
