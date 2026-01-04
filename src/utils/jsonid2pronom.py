"""jsonid2pronom provides a helper script to enable export of generic
JSONID compatible markers to a PRONOM compatible signature file.
"""

import argparse
import asyncio
import copy
import json
import logging
import sys

try:
    from src.jsonid import pronom
except ModuleNotFoundError:
    try:
        from jsonid import pronom
    except ModuleNotFoundError:
        import pronom

# Set up logging.
logging.basicConfig(
    format="%(asctime)-15s %(levelname)s :: %(filename)s:%(lineno)s:%(funcName)s() :: %(message)s",  # noqa: E501
    datefmt="%Y-%m-%d %H:%M:%S",
    level="INFO",
    handlers=[
        logging.StreamHandler(),
    ],
)

logger = logging.getLogger(__name__)


async def load_patterns(path: str) -> list:
    """Load patterns from a file for conversion to a signature file."""
    patterns = []
    with open(path, "r", encoding="utf-8") as patterns_file:
        patterns = json.loads(patterns_file.read())
    return patterns


async def output_signature(path: str):
    """Output JSONID compatible signatures to PRONOM."""

    formats = []

    encodings = ("UTF-8", "UTF-16", "UTF-16BE", "UTF-32LE")
    priorities = []

    increment_id = 0

    markers = await load_patterns(path)

    if not markers:
        logger.error("no patterns provided via path arg")
        sys.exit(1)

    for encoding in encodings:
        increment_id += 1
        json_puid = f"jsonid2pronom/{increment_id}"
        name_ = f"JSONID2PRONOM Conversion ({encoding})"
        try:
            mime = "application/json"
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
            for err_marker in markers:
                logger.debug("--- START ---")
                logger.debug("marker: %s", err_marker)
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
            priorities=list(set(priorities)),
        )
        priorities.append(f"{increment_id}")
        formats.append(fmt)

    pronom.process_formats_to_stdout(formats)


def main() -> None:
    """Primary entry point for this script."""
    parser = argparse.ArgumentParser(
        prog="jsonid2pronom",
        description="convert JSONID compatible markers to PRONOM",
        epilog="for more information visit https://github.com/ffdev-info/jsonid",
    )
    parser.add_argument(
        "--debug",
        help="use debug loggng",
        required=False,
        action="store_true",
    )
    parser.add_argument(
        "--path",
        "-p",
        help="file path to process",
        required=False,
    )
    args = parser.parse_args()
    logging.getLogger(__name__).setLevel(logging.DEBUG if args.debug else logging.INFO)
    logger.debug("debug logging is configured")
    if not args.path:
        parser.print_help(sys.stderr)
        sys.exit()
    asyncio.run(
        output_signature(
            path=args.path,
        )
    )


if __name__ == "__main__":
    main()
