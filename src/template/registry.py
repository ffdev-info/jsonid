"""JSON registry information.

Identifier spec:

    version 0.1:

    A list of data structures is processed in order to determine
    what kind of JSON document we might be looking at.

    version 0.1 is currently designed to identify existence of
    information. It doesn't currently test for negations of
    information, however, this could be introduced, e.g. if a user
    expects one value, but IT CANNOT BE another value, e.g. to
    reduce conflicts/false-positives.

    Keywords (case insensitive):

       * KEY
       * CONTAINS
       * STARTSWITH
       * ENDSWITH
       * IS
       * REGEX
       * EXISTS

       Special:

       * NOEXIST (must be used in conjunction with another keyword)

    ```e.g.
        [
            { "KEY": "name", "IS": "value" },
            { "KEY": "schema", "CONTAINS": "/schema/version/1.1/" },
            { "KEY": "data", "IS": { "more": "data" } },
        ]
    ```


"""

import json
import logging
from dataclasses import dataclass, field
from typing import Final, Optional

try:
    import registry_matchers
except ModuleNotFoundError:
    try:
        from src.template import registry_matchers
    except ModuleNotFoundError:
        from templte import registry_matchers


logger = logging.getLogger(__name__)


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


class IdentificationFailure(Exception):
    """Raise when identification fails."""


NIL_ENTRY: Final[RegistryEntry] = RegistryEntry()

IS_JSON: Final[str] = "parses as JSON but might not conform to a schema"

TYPE_STRING: Final[list] = [{"@en": "data is string type"}]
TYPE_LIST: Final[list] = [{"@en": "data is list type"}]
TYPE_DICT: Final[list] = [{"@en": "data is dict type"}]
TYPE_NONE: Final[list] = [{"@en": "data is null"}]
TYPE_FLOAT: Final[list] = [{"@en": "data is float type"}]
TYPE_INT: Final[list] = [{"@en": "data is integer type"}]
TYPE_BOOL: Final[list] = [{"@en": "data is boolean type"}]
TYPE_ERR: Final[list] = [{"@en": "error processing data"}]


JSON_ONLY: Final[RegistryEntry] = RegistryEntry(
    identifier="id0",
    name=[{"@en": "JavaScript Object Notation (JSON)"}],
    description=[{"@en": IS_JSON}],
    version=None,
    pronom="fmt/817",
    mime=["application/json"],
    markers=None,
)

_registry = [
    RegistryEntry(),
]


def registry() -> list[RegistryEntry]:
    """Return a registry object to the caller."""
    return _registry


def _get_language(string_field: list[dict], language: str = "@en") -> str:
    """Return a string in a given language from a result string."""
    for value in string_field:
        try:
            return value[language]
        except KeyError:
            pass
    return string_field[0]


def get_additional(data: dict, library: bool) -> str:
    """Return additional characterization information about the JSON
    we encountered.
    """

    # pylint: disable=R0911

    if not data:
        return TYPE_NONE
    if isinstance(data, dict):
        return TYPE_DICT
    if isinstance(data, list):
        return TYPE_LIST
    if isinstance(data, float):
        return TYPE_FLOAT
    if isinstance(data, int):
        if data is True or data is False:
            return TYPE_BOOL
        return TYPE_INT
    if isinstance(data, str):
        if not library:
            return TYPE_STRING
        try:
            logger.debug("library mode decoding JSON from string to confirm is JSON")
            json_loaded = json.loads(data)
            return get_additional(json_loaded, False)
        except json.decoder.JSONDecodeError:
            return TYPE_ERR
    return TYPE_ERR


def process_markers(entry, data) -> bool:
    """Run through the markers for an entry in the registry.
    Attempt to exit early if there isn't a match.
    """

    # pylint: disable=R0911

    logger.debug("markers len: %s", len(entry.markers))
    for marker in entry.markers:
        try:
            _ = marker[registry_matchers.MARKER_CONTAINS]
            return registry_matchers.contains_match(marker, data)
        except KeyError:
            pass
        try:
            _ = marker[registry_matchers.MARKER_STARTSWITH]
            return registry_matchers.startswith_match(marker, data)
        except KeyError:
            pass
        try:
            _ = marker[registry_matchers.MARKER_ENDSWITH]
            return registry_matchers.endswith_match(marker, data)
        except KeyError:
            pass
        try:
            _ = marker[registry_matchers.MARKER_IS]
            return registry_matchers.is_match(marker, data)
        except KeyError:
            pass
        try:
            _ = marker[registry_matchers.MARKER_REGEX]
            return registry_matchers.regex_match(marker, data)
        except KeyError:
            pass
        try:
            _ = marker[registry_matchers.MARKER_KEY_EXISTS]
            return registry_matchers.key_exists_match(marker, data)
        except KeyError:
            pass
        try:
            _ = marker[registry_matchers.MARKER_KEY_NO_EXIST]
            return registry_matchers.key_no_exist_match(marker, data)
        except KeyError:
            pass
    return False


def matcher(data: dict, library=True) -> list:
    """Matcher for registry objects"""
    logger.debug("type: '%s'", type(data))
    reg = registry()
    matches = []
    for idx, entry in enumerate(reg):
        logger.debug("processing registry entry: %s", idx)
        match = process_markers(entry, data)
        if not match:
            continue
        if entry in matches:
            continue
        matches.append(entry)
    if len(matches) == 0 or matches[0] == NIL_ENTRY:
        additional = get_additional(data, library)
        json_only = JSON_ONLY
        json_only.additional = additional
        return [json_only]
    logger.debug(matches)
    return matches
