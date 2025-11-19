"""PRONOM export routines."""

import logging
from typing import Final

try:
    import helpers
    import registry_matchers
except ModuleNotFoundError:
    try:
        from src.jsonid import helpers, registry_matchers
    except ModuleNotFoundError:
        from jsonid import helpers, registry_matchers


logger = logging.getLogger(__name__)


class UnprocessableEntity(Exception):
    """Provide a way to give complete feedback to the caller to allow
    it to exit."""


def _type_to_str(t: type) -> str:
    """todo..."""
    if t == helpers.TYPE_INTEGER or t == helpers.TYPE_FLOAT:
        # how do we represent larger numbers? and do we need to?
        return "[30:39]"
    if t == helpers.TYPE_BOOL:
        # true | false
        return "22(74727565|66616C7365)22"
    if t == helpers.TYPE_STRING:
        # string begins with a double quote and ends in a double quote.
        return "22*22"
    if t == helpers.TYPE_MAP:
        # { == 7B; } == 7D
        return "7B*7D"
    if t == helpers.TYPE_LIST:
        # [ == 5B; ] == 5D
        return "5B*5D"
    if t == helpers.TYPE_NONE:
        # null
        return "6E756C6C"
    # This should only trigger for incorrect values at this point..
    raise UnprocessableEntity(f"type_to_str: {t}")


def _complex_is_type() -> str:
    """todo..."""
    raise UnprocessableEntity("complex IS type")


def _str_to_hex_str(s: str) -> str:
    """todo..."""
    k = ""
    for c in s:
        b = hex(ord(c))
        k = f"{k}{b}"
    return k.replace("0x", "")


def process_markers(markers: list) -> tuple[list | bool]:
    """todo...

    returns a tuple describing the processed value and a flag to
    highlight the result is potentially lossless, e.g. in the case
    of matching types, e.g. strings.

    dict_keys(['CONTAINS'])
    dict_keys(['ENDSWITH'])
    dict_keys(['IS']
    dict_keys(['ISTYPE'])
    dict_keys(['STARTSWITH'])


    key(0-n):(0-n)value

    Need to return something like:

      <ByteSequence Reference="BOFoffset" Sequence="FFD8FFE0{2}4A464946000101(00|01|02)" MinOffset="0" MaxOffset=""/>

    """

    COLON: Final[str] = "3A"
    CURLY_OPEN: Final[str] = "7B"
    SQUARE_OPEN: Final[str] = "5B"
    DOUBLE_QUOTE: Final[str] = "22"
    WS: Final[str] = "(0-10)"

    res = []

    res.append("BOF: {0-4095}7B")

    for idx, marker in enumerate(markers, 2):

        logger.debug("marker: %s", marker)

        if registry_matchers.MARKER_GOTO in marker.keys():
            # first key exists like regular key, then we have to
            # search for the next key...
            k0 = _str_to_hex_str(marker["GOTO"])
            k1 = _str_to_hex_str(marker["KEY"])
            k0 = f"{DOUBLE_QUOTE}{k0}{DOUBLE_QUOTE}"
            k1 = f"{DOUBLE_QUOTE}{k1}{DOUBLE_QUOTE}"
            k1 = f"{k0}{WS}{COLON}*{WS}{k1}{WS}{COLON}"
            marker.pop("KEY")
        if registry_matchers.MARKER_INDEX in marker.keys():
            # first we have a square bracket that then needs a search
            # parameter for the next object (curly bracket) and then
            # key...
            k0 = SQUARE_OPEN
            k1 = _str_to_hex_str(marker["KEY"])
            k1 = f"{WS}{k0}*{CURLY_OPEN}*{DOUBLE_QUOTE}{k1}{DOUBLE_QUOTE}"
        if "KEY" in marker.keys():
            k1 = _str_to_hex_str(marker["KEY"])
            k1 = f"{DOUBLE_QUOTE}{k1}{DOUBLE_QUOTE}"
            marker.pop("KEY")
        # Given a key, each of the remaining rule parts must result in
        # exiting early.
        if registry_matchers.MARKER_KEY_EXISTS in marker.keys():
            res.append(f"BOF: k.{k1}{WS}{COLON}".upper())
            continue
        if registry_matchers.MARKER_IS_TYPE in marker.keys():
            t = _type_to_str(marker["ISTYPE"])
            k1 = f"BOF: k.{k1}{WS}{COLON}{WS} v.{t}"
            res.append(k1.upper())
            continue
        if registry_matchers.MARKER_IS in marker.keys():
            marker_is = marker["IS"]
            if not isinstance(marker_is, str):
                _complex_is_type()
            k2 = _str_to_hex_str(marker_is)
            isk = f"BOF: k.{k1}{WS}{COLON}{WS} v.{k2}"
            res.append(isk.upper())
            continue
        if registry_matchers.MARKER_STARTSWITH in marker.keys():
            k2 = _str_to_hex_str(marker["STARTSWITH"])
            isk = f"BOF: k.{k1}{WS}{COLON}{WS} v.22{k2}"
            res.append(isk.upper())
            continue
        if registry_matchers.MARKER_ENDSWITH in marker.keys():
            k2 = _str_to_hex_str(marker["ENDSWITH"])
            isk = f"BOF: k.{k1}{WS}{COLON}{WS} v.*{k2}22"
            res.append(isk.upper())
            continue
        if registry_matchers.MARKER_CONTAINS in marker.keys():
            k2 = _str_to_hex_str(marker["CONTAINS"])
            isk = f"BOF: k.{k1}{WS}{COLON}{WS} v.*{k2}*"
            res.append(isk.upper())
            continue
        if registry_matchers.MARKER_REGEX in marker.keys():
            raise UnprocessableEntity("REGEX not yet implemented")
        if registry_matchers.MARKER_KEY_NO_EXIST in marker.keys():
            raise UnprocessableEntity("KEY NO EXIST not yet implemented")
    res.append("EOF: 7D{0-4095}")
    # Debug logging to demonstrate output.
    for idx, item in enumerate(res, 1):
        logger.debug("%s. %s", idx, item)
    return res
