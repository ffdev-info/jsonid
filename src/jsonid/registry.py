"""JSON registry processor. """

import json
import logging
from typing import Final

try:
    import registry_data
    import registry_matchers
except ModuleNotFoundError:
    try:
        from src.jsonid import registry_data, registry_matchers
    except ModuleNotFoundError:
        from jsonid import registry_data, registry_matchers


logger = logging.getLogger(__name__)


class IdentificationFailure(Exception):
    """Raise when identification fails."""


NIL_ENTRY: Final[registry_data.RegistryEntry] = registry_data.RegistryEntry()

IS_JSON: Final[str] = "parses as JSON but might not conform to a schema"

TYPE_LIST: Final[list] = [{"@en": "data is list type"}]
TYPE_DICT: Final[list] = [{"@en": "data is dict type"}]
TYPE_NONE: Final[list] = [{"@en": "data is null"}]
TYPE_FLOAT: Final[list] = [{"@en": "data is float type"}]
TYPE_INT: Final[list] = [{"@en": "data is integer type"}]
TYPE_BOOL: Final[list] = [{"@en": "data is boolean type"}]
TYPE_ERR: Final[list] = [{"@en": "error processing data"}]


JSON_ONLY: Final[registry_data.RegistryEntry] = registry_data.RegistryEntry(
    identifier="id0",
    name=[{"@en": "JavaScript Object Notation (JSON)"}],
    description=[{"@en": IS_JSON}],
    version=None,
    pronom="fmt/817",
    mime=["application/json"],
    markers=None,
)


def _get_language(string_field: list[dict], language: str = "@en") -> str:
    """Return a string in a given language from a result string."""
    for value in string_field:
        try:
            return value[language]
        except KeyError:
            pass
    return string_field[0]


def get_additional(data: dict) -> str:
    """Return additional characterization information about the JSON
    we encountered.
    """

    # pylint: disable=R0911

    if not data:
        if data is False:
            return TYPE_BOOL
        return TYPE_NONE
    if isinstance(data, dict):
        return TYPE_DICT
    if isinstance(data, list):
        return TYPE_LIST
    if isinstance(data, float):
        return TYPE_FLOAT
    if isinstance(data, int):
        if data is True:
            return TYPE_BOOL
        return TYPE_INT
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


def matcher(data: dict) -> list:
    """Matcher for registry objects"""
    logger.debug("type: '%s'", type(data))
    if isinstance(data, str):
        try:
            data = json.loads(data)
        except json.decoder.JSONDecodeError as err:
            logger.error("unprocessable data: %s", err)
            return []
    reg = registry_data.registry()
    matches = []
    for idx, entry in enumerate(reg):
        try:
            logger.debug("processing registry entry: %s", idx)
            match = process_markers(entry, data)
            if not match:
                continue
            if entry in matches:
                continue
            matches.append(entry)
        except TypeError:
            break
    if len(matches) == 0 or matches[0] == NIL_ENTRY:
        additional = get_additional(data)
        json_only = JSON_ONLY
        json_only.additional = additional
        return [json_only]
    logger.debug(matches)
    return matches
