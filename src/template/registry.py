"""JSON registry information."""

from dataclasses import dataclass, field
from typing import Final

IS_JSON: Final[str] = "parses as JSON but might not conform to a schema"


@dataclass
class RegistryEntry:
    """Class that represents information that might be derived from
    a registry.
    """

    identifier: str = ""
    name: str = ""
    version: str = ""
    markers: dict = field(default_factory=dict)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return False


class IdentificationFailure(Exception):
    """Raise when identification fails."""


NIL_ENTRY: Final[RegistryEntry] = RegistryEntry()

_registry = [
    RegistryEntry(),
    RegistryEntry(),
]


def registry() -> list[RegistryEntry]:
    """Return a registry object to the caller."""
    return _registry


def matcher(data: dict) -> list:
    """Matcher for registry objects"""
    reg = registry()
    matches = []
    for entry in reg:
        for marker_key, marker_value in entry.markers.items():
            try:
                source_value = data[marker_key]
                if source_value:
                    if source_value != marker_value:
                        break
                matches.append(entry)
            except IndexError:
                pass
    return matches
