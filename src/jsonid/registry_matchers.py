"""Functions to support processing of the registry."""

import logging
import re
from typing import Final

logger = logging.getLogger(__name__)

MARKER_INDEX: Final[str] = "INDEX"
MARKER_GOTO: Final[str] = "GOTO"
MARKER_KEY: Final[str] = "KEY"
MARKER_CONTAINS: Final[str] = "CONTAINS"
MARKER_STARTSWITH: Final[str] = "STARTSWITH"
MARKER_ENDSWITH: Final[str] = "ENDSWITH"
MARKER_IS: Final[str] = "IS"
MARKER_REGEX: Final[str] = "REGEX"
MARKER_KEY_EXISTS: Final[str] = "EXISTS"
MARKER_KEY_NO_EXIST: Final[str] = "NOEXIST"
MARKER_IS_TYPE: Final[str] = "ISTYPE"


def at_index(marker: dict, data: dict) -> dict:
    """Provide an ability to investigate an indeex."""
    idx = marker[MARKER_INDEX]
    try:
        data = data[idx]
        return data
    except IndexError:
        return data


def at_goto(marker: dict, data: dict) -> dict:
    """Match data against a regular expression."""
    k = marker[MARKER_GOTO]
    try:
        return data[k]
    except KeyError:
        return data


def contains_match(marker: dict, data: dict) -> bool:
    """Match data against a regular expression."""
    k = marker[MARKER_KEY]
    v = None
    try:
        v = data[k]
    except KeyError:
        return False
    if not isinstance(v, str):
        return False
    match_pattern = marker[MARKER_CONTAINS]
    return match_pattern in v


def startswith_match(marker: dict, data: dict) -> bool:
    """Match data against a regular expression."""
    k = marker[MARKER_KEY]
    v = None
    try:
        v = data[k]
    except KeyError:
        return False
    if not isinstance(v, str):
        return False
    match_pattern = marker[MARKER_STARTSWITH]
    return v.startswith(match_pattern)


def endswith_match(marker: dict, data: dict) -> bool:
    """Match data against a regular expression."""
    k = marker[MARKER_KEY]
    v = None
    try:
        v = data[k]
    except KeyError:
        return False
    if not isinstance(v, str):
        return False
    match_pattern = marker[MARKER_ENDSWITH]
    return v.endswith(match_pattern)


def is_match(marker: dict, data: dict) -> bool:
    """Match data against a regular expression."""
    k = marker[MARKER_KEY]
    v = None
    try:
        v = data[k]
    except KeyError:
        return False
    match_pattern = marker[MARKER_IS]
    return v == match_pattern


def is_type(marker: dict, data: dict) -> bool:
    """Match data against type only."""
    k = marker[MARKER_KEY]
    v = None
    try:
        v = data[k]
    except KeyError:
        return False
    match_pattern = marker[MARKER_IS_TYPE]
    try:
        if isinstance(v, match_pattern):
            return True
    except TypeError:
        pass
    return False


def regex_match(marker: dict, data: dict) -> bool:
    """Match data against a regular expression."""
    k = marker[MARKER_KEY]
    v = None
    try:
        v = data[k]
    except KeyError:
        return False
    if not isinstance(v, str):
        return False
    match_pattern = marker[MARKER_REGEX]
    return re.search(match_pattern, v)


def key_exists_match(marker: dict, data: dict) -> bool:
    """Match data against a regular expression."""
    k = marker[MARKER_KEY]
    try:
        data[k]
    except KeyError:
        return False
    return True


def key_no_exist_match(marker: dict, data: dict) -> bool:
    """Match data against a regular expression."""
    k = marker[MARKER_KEY]
    try:
        data[k]
    except KeyError:
        return True
    return False
