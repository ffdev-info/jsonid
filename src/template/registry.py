"""JSON registry information."""

import logging
from dataclasses import dataclass, field
from typing import Final, Optional

logger = logging.getLogger(__name__)

IS_JSON: Final[str] = "parses as JSON but might not conform to a schema"


@dataclass
class RegistryEntry:
    """Class that represents information that might be derived from
    a registry.
    """

    identifier: str = ""
    name: str = ""
    version: Optional[str | None] = None
    description: str = ""
    markers: list = field(default_factory=list)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return False


class IdentificationFailure(Exception):
    """Raise when identification fails."""


NIL_ENTRY: Final[RegistryEntry] = RegistryEntry()

JSON_ONLY: Final[RegistryEntry] = RegistryEntry(
    identifier="id0",
    name="JSONOnly",
    description=IS_JSON,
    version=None,
    markers=None,
)

_registry = [
    RegistryEntry(),
]


def registry() -> list[RegistryEntry]:
    """Return a registry object to the caller."""
    return _registry


def process_markers(entry, data):
    """Todo..."""
    for marker in entry.markers:
        for marker_key, marker_value in marker.items():
            try:
                logger.debug("key: '%s', value: '%s'", marker_key, marker_value)
                source_value = data[marker_key]
                if not marker_value:
                    # values might be optional if we have a key.
                    continue
                if marker_value != source_value:
                    return False
                if source_value != marker_value:
                    return False
            except KeyError:
                return False
    return True


def matcher(data: dict) -> list:
    """Matcher for registry objects"""
    reg = registry()
    matches = []
    for idx, entry in enumerate(reg):
        logger.debug("processing registry entry: %s", idx)
        match = process_markers(entry, data)
        if not match:
            continue
        matches.append(entry)
    if len(matches) == 0 or matches[0] == NIL_ENTRY:
        return [JSON_ONLY]
    logger.debug(matches)
    return matches
