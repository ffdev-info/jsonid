"""Dataclasses for the registry objects."""

from dataclasses import dataclass, field
from typing import Final, Optional

import yaml

JSON_ID: Final[int] = "jrid:0000"


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
    wikidata: str = ""
    loc: str = ""
    archive_team: str = ""
    rfc: str = ""
    mime: list[str] = field(default_factory=list)
    markers: list[dict] = field(default_factory=list)
    depth: int = 0
    additional: str = ""
    encoding: str = ""

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return False

    def __str__(self):
        """Return summary string."""
        if self.identifier == JSON_ID:
            data = {
                "identifiers": [
                    {"rfc": self.rfc},
                    {"pronom": self.pronom},
                    {"loc": self.loc},
                    {"wikidata": self.wikidata},
                ],
                "documentation": [
                    {"archive_team": self.archive_team},
                ],
                "mime": self.mime,
                "name": self.name,
                "depth": self.depth,
                "additional": self.additional,
                "encoding": self.encoding,
            }
            return yaml.dump(data, indent=2, allow_unicode=True).strip()
        data = {
            "identifiers": [
                {"rfc": self.rfc},
                {"pronom": self.pronom},
                {"loc": self.loc},
                {"wikidata": self.wikidata},
            ],
            "documentation": [
                {"archive_team": self.archive_team},
            ],
            "mime": self.mime,
            "name": self.name,
            "additional": self.additional,
            "encoding": self.encoding,
        }
        return yaml.dump(data, indent=2, allow_unicode=True).strip()

    def json(self):
        """Override default __dict__ behavior."""
        obj = self
        new_markers = []
        for marker in obj.markers:
            try:
                replace_me = marker["ISTYPE"]
                if isinstance(replace_me, type):
                    if replace_me.__name__ == "dict":
                        replace_me = "map"
                    elif replace_me.__name__ == "int":
                        replace_me = "integer"
                    elif replace_me.__name__ == "list":
                        replace_me = "list"
                    elif replace_me.__name__ == "str":
                        replace_me = "string"
                marker["ISTYPE"] = replace_me
                new_markers.append(marker)
            except KeyError:
                pass
        if not new_markers:
            return obj.__dict__
        obj.markers = new_markers
        return obj.__dict__
