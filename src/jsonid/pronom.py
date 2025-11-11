"""PRONOM export routines."""

import logging

logger = logging.getLogger(__name__)


def _str_to_hex_str(s: str) -> str:
    """todo..."""

    k = ""
    for c in s:
        b = hex(ord(c))
        k = f"{k}{b}"
    return k.replace("0x", "")


def process_markers(markers: list):
    """todo...

    dict_keys(['CONTAINS'])
    dict_keys(['ENDSWITH'])
    dict_keys(['IS']
    dict_keys(['ISTYPE'])
    dict_keys(['STARTSWITH'])

    """

    print("1. {0-4095}7B")

    for idx, marker in enumerate(markers, 2):

        if "GOTO" in marker.keys():
            logger.error("GOTO not yet handled")
            break
        if "INDEX" in marker.keys():
            logger.error("INDEX not yet handled")
            break

        k1 = _str_to_hex_str(marker["KEY"])

        # how to model whitespace?
        s = f"22{k1.upper()}22"

        if "EXISTS" in marker.keys():
            print(f"{idx}.", s)
            continue

        if "ISTYPE" in marker.keys():
            logger.info("no idea how to handle ISTYPE...")
            """
            boolean == true/false
            int == lexicographically between 30 and 39? 0 and 65000?
            string... length is a problem...
            list == begins with [
            dict == begins with {
            """
            break

        if "IS" in marker.keys():
            k2 = _str_to_hex_str(marker["KEY"])
            isk = f"{idx}. 22{k2}22"
            print(isk)
            continue

        if "STARTSWITH" in marker.keys():
            k2 = _str_to_hex_str(marker["KEY"])
            isk = f"{idx}. 22{k2}"
            print(isk)
            continue

        if "ENDSWITH" in marker.keys():
            k2 = _str_to_hex_str(marker["KEY"])
            isk = f"{idx}. {k2}22"
            print(isk)
            continue

        if "CONTAINS" in marker.keys():
            k2 = _str_to_hex_str(marker["KEY"])
            isk = f"{idx}. *{k2}*"
            print(isk)
            continue

        marker.pop("KEY")
        print(marker.keys())
