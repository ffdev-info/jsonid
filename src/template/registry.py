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


def _process_markers(entry, data):
    """Todo..."""
    for marker in entry.markers:
        for MARKER_KEY, marker_value in marker.items():
            try:
                logger.debug("key: '%s', value: '%s'", MARKER_KEY, marker_value)
                source_value = data[MARKER_KEY]
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
            _ = marker[registry_matchers.MARKER_KEY_no_exist]
            return registry_matchers.key_no_exist_match(marker, data)
        except KeyError:
            pass
    return False


def matcher(data: dict) -> list:
    """Matcher for registry objects"""
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
        return [JSON_ONLY]
    logger.debug(matches)
    return matches
