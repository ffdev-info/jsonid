"""Helpers for the export functions."""

import datetime
from datetime import timezone
from typing import Final
from xml.dom.minidom import parseString

UTC_TIME_FORMAT: Final[str] = "%Y-%m-%dT%H:%M:%SZ"


def get_utc_timestamp_now():
    """Get a formatted UTC timestamp for 'now' that can be used when
    a timestamp is needed.
    """
    return datetime.datetime.now(timezone.utc).strftime(UTC_TIME_FORMAT)


def new_prettify(c):
    """Remove excess newlines from DOM output.

    via: https://stackoverflow.com/a/14493981
    """
    reparsed = parseString(c)
    return "\n".join(
        [
            line
            for line in reparsed.toprettyxml(indent=" " * 2).split("\n")
            if line.strip()
        ]
    )
