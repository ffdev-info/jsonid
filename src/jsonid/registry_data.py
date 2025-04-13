"""JSON registry data."""

from dataclasses import dataclass, field
from typing import Optional


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

    def __str__(self):
        """Return summary string."""
        return f"""{self.identifier}:
      name: {self.name}
      pronom: {self.pronom}
      additional: {self.additional}""".strip()


_registry = [
    RegistryEntry(
        identifier="id0001",
        name=[{"@en": "package lock file"}],
        description=[{"@en": "node manifest file manifestation"}],
        markers=[
            {"KEY": "name", "EXISTS": None},
            {"KEY": "lockfileVersion", "EXISTS": None},
            {"KEY": "packages", "EXISTS": None},
        ],
    ),
    RegistryEntry(
        identifier="id0002",
        name=[{"@en": "ocfl inventory (all versions)"}],
        description=[{"@en": "ocfl inventory file"}],
        markers=[
            {"KEY": "type", "STARTSWITH": "https://ocfl.io/"},
            {"KEY": "type", "CONTAINS": "spec/#inventory"},
            {"KEY": "head", "EXISTS": None},
            {"KEY": "manifest", "EXISTS": None},
        ],
    ),
    RegistryEntry(
        identifier="id0003",
        name=[{"@en": "gocfl config file"}],
        description=[{"@en": "gocfl config file"}],
        markers=[
            {"KEY": "extensionName", "EXISTS": None},
        ],
    ),
    RegistryEntry(
        identifier="id0004",
        name=[{"@en": "dataverse dataset file"}],
        markers=[
            {"KEY": "datasetVersion", "EXISTS": None},
            {"KEY": "publicationDate", "EXISTS": None},
            {"KEY": "publisher", "EXISTS": None},
            {"KEY": "identifier", "EXISTS": None},
        ],
    ),
    RegistryEntry(
        identifier="id0005",
        name=[{"@en": "rocrate (all versions)"}],
        markers=[
            {"KEY": "@context", "STARTSWITH": "https://w3id.org/ro/crate/"},
            {"KEY": "@context", "ENDSWITH": "/context"},
        ],
    ),
    RegistryEntry(
        identifier="id0006",
        name=[{"@en": "ro-crate (1.1)"}],
        markers=[
            {
                "KEY": "@context",
                "IS": [
                    "https://w3id.org/ro/crate/1.1/context",
                    {"@vocab": "http://schema.org/"},
                ],
            },
        ],
    ),
    RegistryEntry(
        identifier="id0007",
        name=[{"@en": "json schema document"}],
        markers=[
            {"KEY": "$schema", "STARTSWITH": "https://json-schema.org/"},
            {"KEY": "$schema", "ENDSSWITH": "/schema"},
            {"KEY": "$defs", "EXISTS": None},
        ],
    ),
    RegistryEntry(
        identifier="id0008",
        name=[{"@en": "iiif image api (all versions)"}],
        markers=[
            {"KEY": "@context", "STARTSWITH": "http://iiif.io/api/image/"},
            {"KEY": "@context", "ENDSSWITH": "/context.json"},
            {"KEY": "type", "CONTAINS": "ImageService"},
            {"KEY": "protocol", "IS": "http://iiif.io/api/image"},
        ],
    ),
    RegistryEntry(
        identifier="id0009",
        name=[{"@en": "JSON-LD (generic)"}],
        markers=[
            {"KEY": "@context", "EXISTS": None},
            {"KEY": "id", "EXISTS": None},
        ],
    ),
    RegistryEntry(
        identifier="id0010",
        name=[{"@en": "gocfl metafile metadata"}],
        markers=[
            {"KEY": "signature", "EXISTS": None},
            {"KEY": "organisation_id", "EXISTS": None},
            {"KEY": "organisation", "EXISTS": None},
            {"KEY": "title", "EXISTS": None},
            {"KEY": "user", "EXISTS": None},
            {"KEY": "address", "EXISTS": None},
            {"KEY": "created", "EXISTS": None},
            {"KEY": "last_changed", "EXISTS": None},
        ],
    ),
    RegistryEntry(
        identifier="id0011",
        name=[{"@en": "siegfried report (all versions)"}],
        markers=[
            {"KEY": "siegfried", "EXISTS": None},
            {"KEY": "scandate", "EXISTS": None},
            {"KEY": "signature", "EXISTS": None},
            {"KEY": "identifiers", "EXISTS": None},
        ],
    ),
    RegistryEntry(
        identifier="id0012",
        name=[{"@en": "sops encrypted secrets file"}],
        markers=[
            {"KEY": "sopf", "EXISTS": None},
        ],
    ),
    RegistryEntry(
        identifier="id0013",
        name=[{"@en": "sparql query (generic)"}],
        markers=[
            {"KEY": "head", "EXISTS": None},
            {"KEY": "results", "EXISTS": None},
        ],
    ),
    RegistryEntry(
        identifier="id0014",
        name=[{"@en": "wikidata results (generic)"}],
        markers=[
            {"KEY": "head", "EXISTS": None},
            {"KEY": "results", "EXISTS": None},
            {"KEY": "endpoint", "IS": "https://query.wikidata.org/sparql"},
        ],
    ),
    RegistryEntry(
        identifier="id0015",
        name=[{"@en": "google link file"}],
        pronom="fmt/1073",
        markers=[
            {"KEY": "url", "startswith": "https://docs.google.com/open"},
        ],
    ),
    # Also: id can be "bookmarks.json", "inbox.json", "likes.json"
    RegistryEntry(
        identifier="id0016",
        name=[{"@en": "activity streams json (generic)"}],
        markers=[
            {"KEY": "@context", "startswith": "https://www.w3.org/ns/activitystreams"},
            {"KEY": "id", "EXISTS": None},
        ],
    ),
]


def registry() -> list[RegistryEntry]:
    """Return a registry object to the caller."""
    return _registry
