"""Provide lookup functions for the registry."""

import logging

try:
    import registry
    import registry_data
except ModuleNotFoundError:
    try:
        from src.jsonid import registry, registry_data
    except ModuleNotFoundError:
        from jsonid import registry, registry_data


logger = logging.getLogger(__name__)


def lookup_entry(ref: str):
    """Provides lookup functions for JSONID to simplify results output."""
    if ref not in registry.REGISTERED:
        ref = ref.lower()
        reg = registry_data.registry()
        for item in reg:
            if ref != item.identifier:
                continue
            print(item)
            return
        logger.error("registry lookup for ref '%s': no entry found", ref)
        return
    if ref == registry.DOCTYPE_JSON:
        print(registry.JSON_ONLY)
        return
    if ref == registry.DOCTYPE_JSONL:
        print(registry.JSONL_ONLY)
        return
    if ref == registry.DOCTYPE_YAML:
        print(registry.YAML_ONLY)
        return
    if ref == registry.DOCTYPE_TOML:
        print(registry.TOML_ONLY)
        return
