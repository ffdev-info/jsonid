"""PRONOM export routines."""

import logging

logger = logging.getLogger(__name__)


class UnprocessableEntity(Exception):
    """Provide a way to give complete feedback to the caller to allow
    it to exit."""


def _type_to_str(t: type) -> str:
    """todo..."""
    if t == "integer":
        # how do we represent larger numbers?
        return "[30:39]"
    if t == "bool":
        # true | false
        return "22(74727565|66616C7365)22"
    raise UnprocessableEntity(f"{t}")


def _str_to_hex_str(s: str) -> str:
    """todo..."""

    k = ""
    for c in s:
        b = hex(ord(c))
        k = f"{k}{b}"
    return k.replace("0x", "")


def process_markers(markers: list) -> list:
    """todo...

    dict_keys(['CONTAINS'])
    dict_keys(['ENDSWITH'])
    dict_keys(['IS']
    dict_keys(['ISTYPE'])
    dict_keys(['STARTSWITH'])


    key(0-n):(0-n)value

    """

    res = []

    res.append("1. {0-4095}7B")

    for idx, marker in enumerate(markers, 2):

        if "GOTO" in marker.keys():
            logger.error("GOTO not yet handled")
            raise UnprocessableEntity("GOTO")

        if "INDEX" in marker.keys():
            logger.error("INDEX not yet handled")
            raise UnprocessableEntity("INDEX")

        k1 = _str_to_hex_str(marker["KEY"])

        # how to model whitespace?
        s = f"22{k1.upper()}22"

        if "EXISTS" in marker.keys():
            res.append(f"{idx}.{s}")
            continue

        if "ISTYPE" in marker.keys():
            """
            boolean == true/false
            int == lexicographically between 30 and 39? 0 and 65000?
            string... length is a problem...
            list == begins with [
            dict == begins with {
            """
            t = _type_to_str(marker["ISTYPE"])
            k2 = f"{t}"
            res.append(k2)
            continue

        if "IS" in marker.keys():
            k2 = _str_to_hex_str(marker["KEY"])
            isk = f"{idx}. 22{k2}22"
            res.append(isk)
            continue

        if "STARTSWITH" in marker.keys():
            k2 = _str_to_hex_str(marker["KEY"])
            isk = f"{idx}. 22{k2}"
            res.append(isk)
            continue

        if "ENDSWITH" in marker.keys():
            k2 = _str_to_hex_str(marker["KEY"])
            isk = f"{idx}. {k2}22"
            res.append(isk)
            continue

        if "CONTAINS" in marker.keys():
            k2 = _str_to_hex_str(marker["KEY"])
            isk = f"{idx}. *{k2}*"
            res.append(isk)
            continue

        marker.pop("KEY")
        print(marker.keys())

    return res
