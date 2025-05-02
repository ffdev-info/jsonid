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
from typing import Final, Tuple

try:
    import export
    import helpers
    import registry
    import version
except ModuleNotFoundError:
    try:
        from src.jsonid import export, helpers, registry, version
    except ModuleNotFoundError:
        from jsonid import export, helpers, registry, version


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
        logger.debug("(decode) can't process: %s", err)
        return False, None
    return True, data


@helpers.timeit
async def identify_plaintext_bytestream(path: str) -> Tuple[bool, str]:
    """Ensure that the file is a palintext bytestream and can be
    processed as JSON.
    """
    logger.debug("attempting to open: %s", path)
    valid = False

    supported_encodings: Final[list] = [
        "UTF-8",
        "UTF-16",
        "UTF-16LE",
        "UTF-16BE",
        "UTF-32",
        "UTF-32LE",
        "UTF-32BE",
    ]

    for encoding in supported_encodings:
        logger.debug("attempting to open as: %s", encoding)
        with open(path, "r", encoding=encoding) as obj:
            try:
                content = obj.read()
                valid, data = decode(content)
            except UnicodeDecodeError as err:
                logger.debug("(%s) can't process: '%s', err: %s", encoding, path, err)
            except UnicodeError as err:
                logger.debug("(%s) can't process: '%s', err: %s", encoding, path, err)
        if valid:
            return valid, data, encoding

    return False, None, None


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
        valid, data, encoding = await identify_plaintext_bytestream(path)
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
            res = registry.matcher(data, encoding=encoding)
            print(f"file: {path}")
            for item in res:
                print(item)
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
        "--paths",
        "-p",
        help="file path to process",
        required=False,
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
        action="store_true",
    )
    parser.add_argument(
        "--check",
        help="check the registry entrues are correct",
        required=False,
        action="store_true",
    )
    parser.add_argument(
        "--html",
        help="output the registry as html",
        required=False,
        action="store_true",
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
        export.exportJSON()
        sys.exit()
    if args.check:
        if not helpers.entry_check():
            logger.error("registry entries are not correct")
            sys.exit(1)
        sys.exit()
    if args.html:
        helpers.html()
        sys.exit()
    if not args.path:
        parser.print_help(sys.stderr)
        sys.exit()
    asyncio.run(
        process_data(
            path=args.path,
            binary=args.binary,
        )
    )


if __name__ == "__main__":
    main()
