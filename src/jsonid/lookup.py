"""Provide lookup functions for the registry."""

import logging

try:
    import registry
except ModuleNotFoundError:
    try:
        from src.jsonid import registry
    except ModuleNotFoundError:
        from jsonid import registry


# TODO: enable registry lookup by ID/Reference.
# TODO: base entries not in the registry, i.e. TOML/JSON/YAML/JSONL
#       base formats must also be included.

logger = logging.getLogger(__name__)


def lookup_entry(ref: str):
    """Provides lookup functions for the"""
    if ref not in registry.registered:
        ref = ref.lower()
        logger.info("looking up... %s", ref)
        return
    logger.info("looking up core entry: %s", ref)
    raise NotImplementedError("registry lookup not yet implemented")
