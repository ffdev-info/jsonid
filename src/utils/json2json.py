"""json2json will convert JSON compatible objects from one encoding
to UTF-8.
"""

import argparse
import asyncio
import glob
import json
import logging
import os
import sys
from typing import Tuple

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


async def identify_plaintext_bytestream(path: str) -> Tuple[bool, str]:
    """Ensure that the file is a palintext bytestream and can be
    processed as JSON.
    """
    logger.debug("attempting to open: %s", path)
    with open(path, "r", encoding="utf-8") as obj:
        try:
            content = obj.read()
            json_data = json.loads(content)
            return True, json_data
        except UnicodeDecodeError:
            pass
        except json.decoder.JSONDecodeError:
            pass
    with open(path, "r", encoding="utf-16") as obj:
        try:
            content = obj.read()
            json_data = json.loads(content)
            return True, json_data
        except UnicodeError:
            pass
        except json.decoder.JSONDecodeError:
            pass
    with open(path, "r", encoding="utf-16LE") as obj:
        try:
            content = obj.read()
            json_data = json.loads(content)
            return True, json_data
        except UnicodeDecodeError:
            pass
        except json.decoder.JSONDecodeError:
            pass
    return False, None


async def identify_json(paths: list[str]):
    """Identify objects"""
    for idx, path in enumerate(paths):
        valid, data = await identify_plaintext_bytestream(path)
        if not valid:
            continue
        print(json.dumps(data, indent=2))


async def create_manifest(path: str) -> list[str]:
    """Get a list of paths to process."""
    paths = []
    for root, _, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            logger.debug(file_path)
            paths.append(file_path)
    return paths


async def process_glob(glob_path: str):
    """Process glob patterns provided by the user."""
    paths = []
    for path in glob.glob(glob_path):
        if os.path.isdir(path):
            paths = paths + await create_manifest(path)
        if os.path.isfile(path):
            paths.append(path)
    await identify_json(paths)


async def process_data(path: str):
    """Process all objects at a given path"""
    logger.debug("processing: %s", path)

    if "*" in path:
        return await process_glob(path)
    if not os.path.exists(path):
        logger.error("path: '%s' does not exist", path)
        sys.exit(1)
    if os.path.isfile(path):
        await identify_json([path])
        sys.exit(0)
    paths = await create_manifest(path)
    if not paths:
        logger.info("no files in directory: %s", path)
        sys.exit(1)
    await identify_json(paths)


def main() -> None:
    """Primary entry point for this script."""
    parser = argparse.ArgumentParser(
        prog="json2json",
        description="parse JSON UTF-16 (BE-LE) objects and output them as UTF-8 for the sake of developer ergonomics",
        epilog="for more information visit https://github.com/ffdev-info/json-id",
    )
    parser.add_argument(
        "--debug",
        help="use debug loggng",
        required=False,
        action="store_true",
    )
    parser.add_argument(
        "--path",
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
        process_data(
            path=args.path,
        )
    )


if __name__ == "__main__":
    main()
