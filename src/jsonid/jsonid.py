"""jsonid entry-point."""

import argparse
import asyncio
import datetime
import glob
import json
import logging
import os
import sys
import time
from datetime import timezone
from typing import Tuple

try:
    import helpers
    import registry
    import version
except ModuleNotFoundError:
    try:
        from src.jsonid import helpers, registry, version
    except ModuleNotFoundError:
        from jsonid import helpers, registry, version


# Set up logging.
logging.basicConfig(
    format="%(asctime)-15s %(levelname)s :: %(filename)s:%(lineno)s:%(funcName)s() :: %(message)s",  # noqa: E501
    datefmt="%Y-%m-%d %H:%M:%S",
    level="INFO",
    handlers=[
        logging.StreamHandler(),
    ],
)

# Format logs using UTC time.
logging.Formatter.converter = time.gmtime


logger = logging.getLogger(__name__)


def decode(content: str):
    """Decode the given content stream."""
    data = ""
    try:
        data = json.loads(content)
    except json.decoder.JSONDecodeError as err:
        logger.debug("can't process: %s", err)
        return False, None
    return True, data


@helpers.timeit
async def identify_plaintext_bytestream(path: str) -> Tuple[bool, str]:
    """Ensure that the file is a palintext bytestream and can be
    processed as JSON.
    """
    logger.debug("attempting to open: %s", path)
    with open(path, "r", encoding="utf-8") as obj:
        try:
            content = obj.read()
            return decode(content)
        except UnicodeDecodeError as err:
            logger.debug("can't process: %s", err)
            return False, None


def get_date_time() -> str:
    """Return a datetime string for now(),"""
    return datetime.datetime.now(timezone.utc).strftime(version.UTC_TIME_FORMAT)


def version_header() -> str:
    """Output a formatted version header."""
    return f"""jsonid: {version.get_version()}
scandate: {get_date_time()}""".strip()


async def identify_json(paths: list[str], binary: bool):
    """Identify objects"""
    for idx, path in enumerate(paths):
        if os.path.getsize(path) == 0:
            logger.debug("'%s' is an empty file")
            if binary:
                logger.warning("report on binary object...")
            continue
        valid, data = await identify_plaintext_bytestream(path)
        if not valid:
            logger.debug("%s: is not plaintext", path)
            if binary:
                logger.warning("report on binary object...")
            continue
        if data != "":
            logger.debug("processing: %s", path)
            if idx == 0:
                print("---")
                print(version_header())
                print("---")
            res = registry.matcher(data)
            print(f"file: {path}")
            print("identifiers:")
            for item in res:
                print("  ", item)
            print("---")


async def create_manifest(path: str) -> list[str]:
    """Get a list of paths to process."""
    paths = []
    for root, _, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            logger.debug(file_path)
            paths.append(file_path)
    return paths


async def process_glob(glob_path: str, binary: bool):
    """Process glob patterns provided by the user."""
    paths = []
    for path in glob.glob(glob_path):
        if os.path.isdir(path):
            paths = paths + await create_manifest(path)
        if os.path.isfile(path):
            paths.append(path)
    await identify_json(paths, binary)


async def process_data(path: str, binary: bool):
    """Process all objects at a given path"""
    logger.debug("processing: %s", path)

    if "*" in path:
        return await process_glob(path, binary)
    if not os.path.exists(path):
        logger.error("path: '%s' does not exist", path)
        sys.exit(1)
    if os.path.isfile(path):
        await identify_json([path], binary)
        sys.exit(0)
    paths = await create_manifest(path)
    if not paths:
        logger.info("no files in directory: %s", path)
        sys.exit(1)
    await identify_json(paths, binary)


def main() -> None:
    """Primary entry point for this script."""
    parser = argparse.ArgumentParser(
        prog="json-id",
        description="proof-of-concept identifier for JSON objects on disk based on identifying valid objects and their key-values",
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
        required=True,
    )
    parser.add_argument(
        "--binary",
        help="report on binary formats as well as plaintext",
        required=False,
        action="store_true",
    )
    parser.add_argument(
        "--registry",
        help="path to a custom registry to lead into memory replacing the default",
        required=False,
    )
    parser.add_argument(
        "--pronom",
        help="return a PRONOM-centric view of the results",
        required=False,
    )
    parser.add_argument(
        "--export",
        help="export the embedded registry",
        required=False,
    )
    parser.add_argument(
        "--language",
        help="return results in different languages",
        required=False,
    )
    args = parser.parse_args()
    logging.getLogger(__name__).setLevel(logging.DEBUG if args.debug else logging.INFO)
    logger.debug("debug logging is configured")
    if args.registry:
        raise NotImplementedError("custom registry is not yet available")
    if args.pronom:
        raise NotImplementedError("pronom view is not yet implemented")
    if args.language:
        raise NotImplementedError("multiple languages are not yet implemented")
    if args.export:
        raise NotImplementedError("registry export is not yet implemented")
    asyncio.run(
        process_data(
            path=args.path,
            binary=args.binary,
        )
    )


if __name__ == "__main__":
    main()
