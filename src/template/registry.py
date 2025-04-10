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
    markers: dict = field(default_factory=dict)

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


def matcher(data: dict) -> list:
    """Matcher for registry objects"""
    reg = registry()
    matches = []
    for idx, entry in enumerate(reg):
        logger.debug("processing registry entry: %s", idx)
        match = False
        for marker_key, marker_value in entry.markers.items():
            try:
                source_value = data[marker_key]
                if source_value:
                    if source_value == marker_value:
                        match = True
            except IndexError:
                pass
        if match:
            matches.append(entry)
    if len(matches) == 0:
        return [JSON_ONLY]

    logger.debug(matches)
    return matches
