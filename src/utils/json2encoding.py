"""Write a UTF-8 file to a different encoding."""

import argparse
import logging
import sys
import time

from pathlib import Path
from typing import Final

# Set up logging.
logging.basicConfig(
    format="%(asctime)-15s %(levelname)s :: %(filename)s:%(lineno)s:%(funcName)s() :: %(message)s",  # noqa: E501
    datefmt="%Y-%m-%d %H:%M:%S",
    level="INFO",
    handlers=[
        logging.StreamHandler(),
    ],
)


# Default to UTC time.
logging.Formatter.converter = time.gmtime

logger = logging.getLogger(__name__)


supported_encodings: Final[list] = [
    "UTF-8",
    "UTF-16",
    "UTF-16BE",
    "UTF-32",
    "UTF-32BE",
    "SHIFT-JIS",
    "BIG5",
]


def write_json(path: str, output: str, encoding: str):
    """Write files with different encodings."""
    if encoding.upper() not in supported_encodings:
        logger.error(
            "encoding: '%s' not supported, must be one of: '%s'",
            encoding,
            ", ".join(supported_encodings),
        )
        sys.exit(1)
    data = None
    with open(path, "r") as input:
        data = input.read()
    data = data.encode(encoding)
    with open(output, "wb") as output:
        output.write(data)


def main():
    """Primary entry point for this script."""

    parser = argparse.ArgumentParser(
        prog="json2json",
        description="read a plaintext file (usually JSON) and opt to output it in a different encodingss",
        epilog="for more information visit https://github.com/ffdev-info/json-id",
    )
    parser.add_argument(
        "--debug",
        help="use debug loggng",
        required=False,
        action="store_true",
    )
    parser.add_argument(
        "--input",
        "-i",
        help="file path to process",
        required=False,
    )
    parser.add_argument(
        "--output",
        "-o",
        help="output file path",
        required=False,
    )
    parser.add_argument(
        "--encoding",
        "-e",
        help="encoding to output as",
        required=False,
    )
    parser.add_argument(
        "--list",
        "-l",
        help="list encodings",
        required=False,
        action="store_true",
    )
    args = parser.parse_args()
    logging.getLogger(__name__).setLevel(logging.DEBUG if args.debug else logging.INFO)
    logger.debug("debug logging is configured")
    if args.list:
        print("available encodings:", ", ".join(supported_encodings))
        sys.exit()
    if not args.input and args.output:
        parser.print_help(sys.stderr)
        sys.exit()
    write_json(path=args.input, output=args.output, encoding=args.encoding)


if __name__ == "__main__":
    main()
