"""File processing functions."""

import datetime
import glob
import json
import logging
import os
import sys
import tomllib as toml
from datetime import timezone
from typing import Final

import yaml

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

try:
    import analysis
    import base_obj_presets as presets
    import compressionlib
    import helpers
    import output
    import registry
    import version
except ModuleNotFoundError:
    try:
        from src.jsonid import analysis
        from src.jsonid import base_obj_presets as presets
        from src.jsonid import compressionlib, helpers, output, registry, version
    except ModuleNotFoundError:
        from jsonid import analysis
        from jsonid import base_obj_presets as presets
        from jsonid import compressionlib, helpers, output, registry, version


logger = logging.getLogger(__name__)


class NotJSONLError(Exception):
    """Provides an exception to handle when we can't process jsonl."""


# FFB traditionally stands for first four bytes, but of course this
# value might not be 4 in this script.
#
# Minimal optimal read is 4KiB (sector size). We use a multiple of
# that value to optimize disk i/o when we first determine if a file
# is text-based or binary.
#
FFB: Final[int] = 40960

# Minimum no. lines in a JSONL file.
JSONL_MIN_LINES = 1


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
        binary = bool(chr(char).encode().translate(None, text_chars))
        if binary is True:
            return False
    return True


async def whitespace_check(chars: str) -> bool:
    """Check whether the file only contains whitespace.

    NB. this check might take longer than needed.
    """
    if not chars.strip():
        return False
    return True


def _json_processing(content) -> tuple:
    """Provide a wrapper and a way to test JSON processing. We use
    the default JSON mpdule here but we could always swap this out
    for orjson/orjsonl or one of the other high-performance libraries.
    """
    try:
        data = json.loads(content)
        return True, data, registry.DOCTYPE_JSON
    except json.decoder.JSONDecodeError as err:
        logger.debug("(decode) can't process: %s as JSON", err)
    return False, False, False


def _jsonl_processing(content) -> tuple:
    """Provide a wrapper and a way to test JSONL processing. We use
    the default JSON mpdule here but we could always swap this out
    for orjson/orjsonl or one of the other high-performance libraries."""
    try:
        content = content.strip().split("\n")
        if len(content) < JSONL_MIN_LINES:
            raise NotJSONLError("content has only one newline and so is not JSONL")
        # Load each line, one by one, as shown in the orsonjl module.
        data = [json.loads(line) for line in content]
        return True, data, registry.DOCTYPE_JSONL
    except (NotJSONLError, json.decoder.JSONDecodeError) as err:
        logger.debug("(decode) can't process: %s as JSONL", err)
    return False, False, False


def decode(content: str, strategy: list) -> tuple:
    """Decode the given content stream."""
    data = ""
    if registry.DOCTYPE_JSON in strategy:
        valid, content_, type_ = _json_processing(content)
        if valid:
            return valid, content_, type_
    if registry.DOCTYPE_JSONL in strategy:
        valid, content_, type_ = _jsonl_processing(content)
        if valid:
            return valid, content_, type_
    if registry.DOCTYPE_YAML in strategy:
        try:
            if content.strip()[:3] != "---":
                raise TypeError
            data = yaml.load(content.strip(), Loader=Loader)
            if not isinstance(data, str):
                return True, data, registry.DOCTYPE_YAML
        except (
            yaml.scanner.ScannerError,
            yaml.parser.ParserError,
            yaml.reader.ReaderError,
            yaml.composer.ComposerError,
        ) as err:
            logger.debug("(decode) can't process: %s", err)
        except (TypeError, IndexError):
            # Document too short, or YAML without header is not supported.
            pass
    if registry.DOCTYPE_TOML in strategy:
        try:
            data = toml.loads(content)
            return True, data, registry.DOCTYPE_TOML
        except toml.TOMLDecodeError as err:
            logger.debug("(decode) can't process: %s", err)
    return False, None, None


def get_date_time() -> str:
    """Return a datetime string for now(),"""
    return datetime.datetime.now(timezone.utc).strftime(version.UTC_TIME_FORMAT)


def version_header() -> str:
    """Output a formatted version header."""
    return f"""jsonid: {version.get_version()}
scandate: {get_date_time()}""".strip()


async def analyse_json(paths: list[str], strategy: list):
    """Analyse a JSON object."""
    analysis_res = []
    for path in paths:
        if os.path.getsize(path) == 0:
            logger.debug("%s is an empty file", path)
            continue
        base_obj = await identify_plaintext_bytestream(
            path=path,
            strategy=strategy,
            analyse=True,
        )
        if not base_obj.valid:
            logger.debug("%s: is not plaintext", path)
            continue
        if base_obj.data == "" or base_obj.data is None:
            continue
        res = await analysis.analyse_input(base_obj.data, base_obj.content_for_analysis)
        res["doctype"] = base_obj.doctype
        res["encoding"] = base_obj.encoding
        res["agent"] = version.get_agent()
        if base_obj.doctype == registry.DOCTYPE_JSONL:
            res["compression"] = base_obj.compression
            res.pop("content_length")
            res.pop("depth")
            res.pop("heterogeneous_list_types")
            res.pop("line_warning")
            res.pop("top_level_types")
            res.pop("top_level_keys")
            res.pop("top_level_keys_count")
        analysis_res.append(res)
    return analysis_res


# pylint: disable=R0913,R0917
async def process_result(
    path: str,
    base_obj: registry.BaseCharacteristics,
    padding: int,
    agentout: bool,
):
    """Process something JSON/YAML/TOML"""
    results = []
    # NB. these switch-like ifs might not be needed in the fullness
    # of time. It depends if we need to do any custom processing of
    # any of the formats registered. We may want to consider removing
    # these before releasing v1.0.0.
    if base_obj.empty or base_obj.binary:
        output.output_results(
            path=path,
            results=[base_obj],
            padding=padding,
            agentout=agentout,
        )
        return
    if not base_obj.valid:
        output.output_results(
            path=path,
            results=[base_obj],
            padding=padding,
            agentout=agentout,
        )
        return
    # If we don't exit early and we try and identify the file... we then
    # create a new class object with an identification...
    if base_obj.doctype == registry.DOCTYPE_JSON:
        results = registry.matcher(base_obj)
    if base_obj.doctype == registry.DOCTYPE_JSONL:
        results = registry.matcher(base_obj)
    if base_obj.doctype == registry.DOCTYPE_YAML:
        results = registry.matcher(base_obj)
    if base_obj.doctype == registry.DOCTYPE_TOML:
        results = registry.matcher(base_obj)
    output.output_results(
        path=path,
        results=results,
        padding=padding,
        agentout=agentout,
    )
    return


def _get_padding(paths: list):
    """Determine the amount of padding required to pretty-print resuis not plainlts
    to the console when they are available.
    """
    padding = 0
    for path in paths:
        fname = os.path.basename(path)
        if not len(fname) > padding:
            continue
        padding = len(fname)
    return padding


async def identify_json(paths: list[str], strategy: list, binary: bool, agentout: bool):
    """Identify objects."""
    padding = _get_padding(paths=paths)
    for _, path in enumerate(paths):
        if os.path.getsize(path) == 0:
            logger.debug("%s is an empty file", path)
            base_obj = registry.BaseCharacteristics(empty=True)
            if binary:
                await process_result(
                    path=path,
                    base_obj=base_obj,
                    padding=padding,
                    agentout=agentout,
                )
            continue
        base_obj = await identify_plaintext_bytestream(
            path=path,
            strategy=strategy,
            analyse=False,
        )
        if not base_obj.valid:
            logger.debug("%s: is not plaintext", path)
            if binary:
                await process_result(
                    path=path,
                    base_obj=base_obj,
                    padding=padding,
                    agentout=agentout,
                )
            continue
        logger.debug("processing: %s (%s)", path, base_obj.doctype)
        await process_result(
            path=path,
            base_obj=base_obj,
            padding=padding,
            agentout=agentout,
        )


async def open_and_decode(path: str, strategy: list) -> registry.BaseCharacteristics:
    """Attempt to open a given file and decode it as JSON."""
    content = None
    compression = None
    if not os.path.getsize(path):
        logger.debug("file is zero bytes: %s", path)
        return presets.no_id_empty()
    with open(path, "rb") as json_stream:
        first_chars = json_stream.read(FFB)
        if not await text_check(first_chars):
            if registry.DOCTYPE_JSONL not in strategy:
                return presets.no_id_binary()
            # If not text, check at least for compression. We might
            # have a compressed JSONL file.
            compression = await compressionlib.compress_check(first_chars)
            if not compression:
                return presets.no_id_binary()
        # Read the content whether we have compression or not.
        if not compression:
            content = first_chars + json_stream.read()
        elif compression:
            content = await compressionlib.decompress_stream(
                path=path, compression=compression
            )
            if not content:
                return presets.no_id_compression(compression=compression)
        # We have content, but it might only be whitespace.
        if not await whitespace_check(content):
            return presets.no_id_whitespace()
        # We have something we can try to identify.
        return presets.possible_id(
            content=content,
            compression=compression,
        )


@helpers.timeit
async def identify_plaintext_bytestream(
    path: str, strategy: list, analyse: bool = False
) -> registry.BaseCharacteristics:
    """Ensure that the file is a palintext bytestream and can be
    processed as JSON.

    If analysis is `True` we try to return more low-level file
    information to help folks make appraisal decisions.

    Encodings in Python are split into the following, where UTF-32 on
    its own is a little confusing. If WE are writing the encoding then
    I believe it leaves off the byte-order-marker and we want to
    select UTF-32LE to make sure it is written.

    If we are decoding, then I don't think it matters. I think we
    try to decode and if it works it works.

    Encodings:

        "UTF-8",
        "UTF-16",
        "UTF-16LE",
        "UTF-16BE",
        "UTF-32",
        "UTF-32LE",
        "UTF-32BE",
        "SHIFT-JIS",
        "BIG5",

    """

    # pylint: disable=R0911

    logger.debug("attempting to open: %s", path)
    valid = False
    supported_encodings: Final[list] = [
        "UTF-8",
        "UTF-16",
        "UTF-16BE",
        "UTF-32",
        "UTF-32BE",
        "SHIFT-JIS",
        "BIG5",
    ]
    base_obj = await open_and_decode(path, strategy)
    if base_obj.empty:
        return base_obj
    if base_obj.only_whitespace:
        return base_obj
    if base_obj.binary:
        return presets.no_id_binary()
    for encoding in supported_encodings:
        try:
            contents = base_obj.data.decode(encoding)
            valid, data, doctype = decode(contents, strategy)
            if not valid:
                continue
            if not analyse and doctype == registry.DOCTYPE_JSONL:
                # Treat the first line of a JSONL file as the authoritative
                # object type.
                data = data[0]
            if valid and analyse:
                return registry.BaseCharacteristics(
                    valid=valid,
                    data=data,
                    doctype=doctype,
                    encoding=encoding,
                    content_for_analysis=contents,
                    compression=base_obj.compression,
                )
            if valid:
                return registry.BaseCharacteristics(
                    valid=valid,
                    data=data,
                    doctype=doctype,
                    encoding=encoding,
                    compression=base_obj.compression,
                    text=True,
                )
        except (UnicodeDecodeError, UnicodeError) as err:
            logger.debug("(%s) can't process: '%s', err: %s", encoding, path, err)
    # We haven't any identification to return. Return based on
    # precedent.
    if base_obj.compression:
        return presets.no_id_compression(compression=base_obj.compression)
    if base_obj.text:
        return presets.no_id_text()
    return presets.no_id_binary()


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


async def process_data(path: str, strategy: list, binary: bool, agentout: bool):
    """Process all objects at a given path."""
    logger.debug("processing: %s", path)
    if "*" in path:
        paths = await process_glob(path)
        await identify_json(
            paths=paths,
            strategy=strategy,
            binary=binary,
            agentout=agentout,
        )
        sys.exit(0)
    if not os.path.exists(path):
        logger.error("path: '%s' does not exist", path)
        sys.exit(1)
    if os.path.isfile(path):
        await identify_json(
            paths=[path],
            strategy=strategy,
            binary=binary,
            agentout=agentout,
        )
        sys.exit(0)
    paths = await create_manifest(path)
    if not paths:
        logger.info("no files in directory: %s", path)
        sys.exit(1)
    await identify_json(
        paths=paths,
        strategy=strategy,
        binary=binary,
        agentout=agentout,
    )


async def output_analysis(res: list) -> None:
    """Format the output of the analysis."""
    for item in res:
        print(json.dumps(item, indent=2))


async def analyse_data(path: str, strategy: list) -> list:
    """Process all objects at a given path."""
    logger.debug("processing: %s", path)
    res = []
    if "*" in path:
        paths = await process_glob(path)
        res = await analyse_json(paths=paths, strategy=strategy)
        await output_analysis(res)
        sys.exit()
    if not os.path.exists(path):
        logger.error("path: '%s' does not exist", path)
        sys.exit(1)
    if os.path.isfile(path):
        res = await analyse_json(paths=[path], strategy=strategy)
        await output_analysis(res)
        sys.exit(1)
    paths = await create_manifest(path)
    if not paths:
        logger.info("no files in directory: %s", path)
        sys.exit(1)
    res = await analyse_json(paths=paths, strategy=strategy)
    await output_analysis(res)
    sys.exit()
