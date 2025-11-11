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
    for datum in data:
        print("---")
        pronom.process_markers(datum.json()["markers"])
        # break


def exportPRONOMXML() -> None:
    """Export a PRONOM compatible set of signatures."""
