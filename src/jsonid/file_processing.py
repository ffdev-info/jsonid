"""File processing functions."""

import datetime
import glob
import json
import logging
import os
import sys
from datetime import timezone
from typing import Final, Tuple

try:
    import analysis
    import helpers
    import registry
    import version
except ModuleNotFoundError:
    try:
        from src.jsonid import analysis, helpers, registry, version
    except ModuleNotFoundError:
        from jsonid import analysis, helpers, registry, version


logger = logging.getLogger(__name__)


# FFB traditionally stands for first four bytes, but of course this
# value might not be 4 in this script.
FFB: Final[int] = 42


async def text_check(chars: str) -> bool:
    """Check the first characters of the file to figure out if the
    file is text. Return `True` if the file is text, i.e. no binary
    bytes are detected.

    via. https://stackoverflow.com/a/7392391
    """
    text_chars = bytearray(
        {0, 7, 8, 9, 10, 12, 13, 27} | set(range(0x20, 0x100)) - {0x7F}
    )
    for char in chars:
        is_binary = bool(chr(char).encode().translate(None, text_chars))
        if is_binary is True:
            return False
    return True


def decode(content: str):
    """Decode the given content stream."""
    data = ""
    try:
        data = json.loads(content)
    except json.decoder.JSONDecodeError as err:
        logger.debug("(decode) can't process: %s", err)
        return False, None
    return True, data


def get_date_time() -> str:
    """Return a datetime string for now(),"""
    return datetime.datetime.now(timezone.utc).strftime(version.UTC_TIME_FORMAT)


def version_header() -> str:
    """Output a formatted version header."""
    return f"""jsonid: {version.get_version()}
scandate: {get_date_time()}""".strip()


async def analyse_json(paths: list[str]):
    """Analyse a JSON object."""
    analysis_res = []
    for path in paths:
        if os.path.getsize(path) == 0:
            logger.debug("'%s' is an empty file")
            continue
        valid, data, encoding = await identify_plaintext_bytestream(path)
        if not valid:
            logger.debug("%s: is not plaintext", path)
            continue
        if data == "":
            continue
        await analysis.analyse_input(data)
        analysis_res.append((valid, encoding))
    return analysis_res


async def identify_json(paths: list[str], binary: bool, simple: bool):
    """Identify objects"""
    for idx, path in enumerate(paths):
        if os.path.getsize(path) == 0:
            logger.debug("'%s' is an empty file")
            if binary:
                logger.warning("report on binary object...")
            continue
        valid, data, encoding, _ = await identify_plaintext_bytestream(path)
        if not valid:
            logger.debug("%s: is not plaintext", path)
            if binary:
                logger.warning("report on binary object...")
            continue
        if data == "":
            continue
        logger.debug("processing: %s", path)
        res = registry.matcher(data, encoding=encoding)
        if simple:
            for item in res:
                name_ = item.name[0]["@en"]
                version_ = item.version
                if version_ is not None:
                    name_ = f"{name_}: {version_}"
                print(
                    json.dumps(
                        {
                            "identifier": item.identifier,
                            "filename": os.path.basename(path),
                            "encoding": item.encoding,
                        }
                    )
                )
            continue
        if idx == 0:
            print("---")
            print(version_header())
            print("---")
        print(f"file: {path}")
        for item in res:
            print(item)
        print("---")


@helpers.timeit
async def identify_plaintext_bytestream(path: str) -> Tuple[bool, str, str]:
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
        "SHIFT-JIS",
        "BIG5",
    ]
    copied = None
    with open(path, "rb") as json_stream:
        first_chars = json_stream.read(FFB)
        if not await text_check(first_chars):
            return False, None, None, None
        copied = first_chars + json_stream.read()
    for encoding in supported_encodings:
        try:
            content = copied.decode(encoding)
            valid, data = decode(content)
        except UnicodeDecodeError as err:
            logger.debug("(%s) can't process: '%s', err: %s", encoding, path, err)
        except UnicodeError as err:
            logger.debug("(%s) can't process: '%s', err: %s", encoding, path, err)
        if valid:
            return valid, data, encoding
    return False, None, None


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
    return paths


async def process_data(path: str, binary: bool, simple: bool):
    """Process all objects at a given path"""
    logger.debug("processing: %s", path)

    if "*" in path:
        paths = await process_glob(path)
        await identify_json(paths, binary, simple)
        sys.exit(0)
    if not os.path.exists(path):
        logger.error("path: '%s' does not exist", path)
        sys.exit(1)
    if os.path.isfile(path):
        await identify_json([path], binary, simple)
        sys.exit(0)
    paths = await create_manifest(path)
    if not paths:
        logger.info("no files in directory: %s", path)
        sys.exit(1)
    await identify_json(paths, binary, simple)


async def analyse_data(path: str) -> list:
    """Process all objects at a given path"""
    logger.debug("processing: %s", path)

    if "*" in path:
        paths = await process_glob(path)
        return await analyse_json(paths)
    if not os.path.exists(path):
        logger.error("path: '%s' does not exist", path)
        sys.exit(1)
    if os.path.isfile(path):
        return await analyse_json([path])
    paths = await create_manifest(path)
    if not paths:
        logger.info("no files in directory: %s", path)
        sys.exit(1)
    return await analyse_json(paths)
