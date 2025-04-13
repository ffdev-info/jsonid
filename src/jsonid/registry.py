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


def process_markers(registry_entry: registry_data.RegistryEntry, data: dict) -> bool:
    """Run through the markers for an entry in the registry.
    Attempt to exit early if there isn't a match.
    """

    # pylint: disable=R0911,R0912.R0915

    if isinstance(data, list):
        for marker in registry_entry.markers:
            try:
                _ = marker[registry_matchers.MARKER_INDEX]
                data = registry_matchers.at_index(marker, data)
                break
            except KeyError:
                return False
    for marker in registry_entry.markers:
        try:
            _ = marker[registry_matchers.MARKER_GOTO]
            data = registry_matchers.at_goto(marker, data)
        except KeyError as err:
            logger.debug("following through: %s", err)
        try:
            _ = marker[registry_matchers.MARKER_CONTAINS]
            match = registry_matchers.contains_match(marker, data)
            if not match:
                return False
        except KeyError as err:
            logger.debug("following through: %s", err)
        try:
            _ = marker[registry_matchers.MARKER_STARTSWITH]
            match = registry_matchers.startswith_match(marker, data)
            if not match:
                return False
        except KeyError as err:
            logger.debug("following through: %s", err)
        try:
            _ = marker[registry_matchers.MARKER_ENDSWITH]
            match = registry_matchers.endswith_match(marker, data)
            if not match:
                return False
        except KeyError as err:
            logger.debug("following through: %s", err)
        try:
            _ = marker[registry_matchers.MARKER_IS]
            match = registry_matchers.is_match(marker, data)
            if not match:
                return False
        except KeyError as err:
            logger.debug("following through: %s", err)
        try:
            _ = marker[registry_matchers.MARKER_IS_TYPE]
            match = registry_matchers.is_type(marker, data)
            if not match:
                return False
        except KeyError as err:
            logger.debug("following through: %s", err)
        try:
            _ = marker[registry_matchers.MARKER_REGEX]
            match = registry_matchers.regex_match(marker, data)
            if not match:
                return False
        except KeyError as err:
            logger.debug("following through: %s", err)
        try:
            _ = marker[registry_matchers.MARKER_KEY_EXISTS]
            match = registry_matchers.key_exists_match(marker, data)
            if not match:
                return False
        except KeyError as err:
            logger.debug("following through: %s", err)
        try:
            _ = marker[registry_matchers.MARKER_KEY_NO_EXIST]
            match = registry_matchers.key_no_exist_match(marker, data)
            if not match:
                return False
        except KeyError as err:
            logger.debug("following through: %s", err)
    return True


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
    for idx, registry_entry in enumerate(reg):
        try:
            logger.debug("processing registry entry: %s", idx)
            match = process_markers(registry_entry, data)
            if not match:
                continue
            if registry_entry in matches:
                continue
            matches.append(registry_entry)
        except TypeError as err:
            logger.debug("%s", err)
            continue
    if len(matches) == 0 or matches[0] == NIL_ENTRY:
        additional = get_additional(data)
        json_only = JSON_ONLY
        json_only.additional = additional
        return [json_only]
    logger.debug(matches)
    return matches
