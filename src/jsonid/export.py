"""Functions to support export."""

import datetime
import json
import logging
from datetime import timezone

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


def exportPRONOM() -> None:
    """Export a PRONOM compatible set of signatures."""
    logger.debug("exporting registry as PRONOM")
    data = registry_data.registry()
    all_sequences = []

    formats = []

    for datum in data:
        id_ = datum.json()["identifier"]
        name_ = datum.json()["name"]
        markers = datum.json()["markers"]

        format_sequences = []

        try:
            sequences = pronom.process_markers(markers.copy())
            all_sequences.append((id_, name_, sequences))
            format_sequences.append(sequences)
        except pronom.UnprocessableEntity as err:
            logger.error(
                "%s %s: cannot handle: %s",
                id_,
                name_,
                err,
            )
            for marker in markers:
                logger.debug("--- START ---")
                logger.debug("marker: %s", marker)
                logger.debug("---  END  ---")
            continue

        format = pronom.Format(
            id=0,
            name=name_,
            version="",
            puid=id_,
            mime="TODO",
            classification="structured text",  # TODO: magic
            external_signatures=[
                pronom.ExternalSignature(
                    id=0,
                    signature="JSON",
                    type="TODO",
                )
            ],
            internal_signatures=format_sequences[0],
            priorities=[],
        )

        formats.append(format)

    # Process all the results.
    for sequences in all_sequences:
        if not isinstance(sequences[2], list):
            raise TypeError
        print("-----")
        print(f"{sequences[0]}: {sequences[1][0]["@en"]}")
        print("")
        for idx, sequence in enumerate(sequences[2]):
            # Need to return a set of internal signatures:
            # <InternalSignature ID="67" Specificity="Specific">
            #    ... bytesequences...
            #
            #
            print(idx, ".", sequence.byte_sequences)
        # return

    pronom.process_formats_and_save(formats, "abc.xml")


def exportPRONOMXML() -> None:
    """Export a PRONOM compatible set of signatures."""
