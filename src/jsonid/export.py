"""Functions to support export."""

import copy
import datetime
import json
import logging
from datetime import timezone
from typing import Final

try:
    import pronom
    import registry_data
    import version
except ModuleNotFoundError:
    try:
        from src.jsonid import pronom, registry_data, version
    except ModuleNotFoundError:
        from jsonid import pronom, registry_data, version

logger = logging.getLogger(__name__)


PRONOM_FILENAME: Final[str] = "jsonid_pronom.xml"


class PRONOMException(Exception):
    """Exception class if we can't create a PRONOM signature as expected."""


def exportJSON() -> None:  # pylint: disable=C0103
    """Export to JSON."""
    logger.debug("exporting registry as JSON")
    data = registry_data.registry()
    json_obj = []
    id_ = {
        "jsonid": version.get_version(),
        "entries": len(data),
        "timestamp": int(
            str(datetime.datetime.now(timezone.utc).timestamp()).split(".", maxsplit=1)[
                0
            ]
        ),
    }
    json_obj.append(id_)
    for datum in data:
        json_obj.append(datum.json())
    print(json.dumps(json_obj, indent=2))


def export_pronom() -> None:
    """Export a PRONOM compatible set of signatures.

    Export is done in two phases. A set of proposed "Baseline" JSON
    signatures to catch many JSON instances.

    Second the JSONID registry is exported.

    Every export has a priority over the other so that there should
    be no multiple identification results.
    """

    # pylint: disable=R0914; too-many local variables.

    logger.debug("exporting registry as PRONOM")

    reg_data = registry_data.registry()
    formats = []

    encodings = ("UTF-8", "UTF-16", "UTF-16BE", "UTF-32LE")
    priorities = []

    increment_id = 0

    for encoding in encodings:
        all_baseline = pronom.create_baseline_json_sequences(encoding)
        for baseline in all_baseline:
            increment_id += 1
            fmt = pronom.Format(
                id=increment_id,
                name=f"JSON (Baseline - fmt/817) ({encoding})",
                version="",
                puid="jsonid:0000",
                mime="application/json",
                classification="structured text",
                external_signatures=[
                    pronom.ExternalSignature(
                        id=increment_id,
                        signature="json",
                        type=pronom.EXT,
                    )
                ],
                internal_signatures=[baseline],
                priorities=priorities,
            )
            priorities.append(f"{increment_id}")
            formats.append(fmt)

    for encoding in encodings:
        for entry in reg_data:
            increment_id += 1
            json_puid = f"{entry.json()['identifier']};{encoding}"
            name_ = f"{entry.json()['name'][0]['@en']} ({encoding})"
            markers = entry.json()["markers"]
            try:
                mime = entry.json()["mime"][0]
            except IndexError:
                mime = ""
            try:
                sequences = pronom.process_markers(
                    copy.deepcopy(markers),
                    increment_id,
                    encoding=encoding,
                )
            except pronom.UnprocessableEntity as err:
                logger.error(
                    "%s %s: cannot handle: %s",
                    json_puid,
                    name_,
                    err,
                )
                for marker in markers:
                    logger.debug("--- START ---")
                    logger.debug("marker: %s", marker)
                    logger.debug("---  END  ---")
                continue
            fmt = pronom.Format(
                id=increment_id,
                name=name_,
                version="",
                puid=json_puid,
                mime=mime,
                classification="structured text",
                external_signatures=[
                    pronom.ExternalSignature(
                        id=increment_id,
                        signature="json",
                        type=pronom.EXT,
                    )
                ],
                internal_signatures=sequences,
                priorities=copy.deepcopy(list(set(priorities))),
            )
            priorities.append(f"{increment_id}")
            formats.append(fmt)

    pronom.process_formats_and_save(formats, PRONOM_FILENAME)
