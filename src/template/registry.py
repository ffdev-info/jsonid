"""JSON registry information."""

from dataclasses import dataclass, field
from typing import Final

IS_JSON: Final[str] = "parses as JSON but might not conform to a schema"

@dataclass
class RegistryEntry():
    """Class that represents information that migth be derived from
    a registry.
    """
    identifier: str = ""
    name: str = ""
    version: str = ""
    markers: dict = field(default_factory=dict)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False


class IdentificationFailure(Exception):
    """Raise when identification fails."""


NilEntry: Final[RegistryEntry] = RegistryEntry()

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
        for key, value in entry.markers.items():
            try:
                v = data[key]
                if value:
                    if v != value:
                        break
                matches.append(entry)
            except IndexError:
                pass
    return matches
