"""JSON registry data."""

from dataclasses import dataclass, field
from typing import Final, Optional

@dataclass
class RegistryEntry:  # pylint: disable=R0902
    """Class that represents information that might be derived from
    a registry.
    """

    identifier: str = ""
    name: list = field(default_factory=list)
    version: Optional[str | None] = None
    description: list = field(default_factory=list)
    pronom: str = ""
    mime: list[str] = field(default_factory=list)
    markers: list[dict] = field(default_factory=list)
    additional: str = ""

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return False

_registry = [
    RegistryEntry(),
]

def registry() -> list[RegistryEntry]:
    """Return a registry object to the caller."""
    return _registry
