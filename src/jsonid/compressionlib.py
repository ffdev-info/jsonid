"""Handlers for compression."""

import bz2
import gzip
import logging
import os
from typing import Any, Final

magic = None  # pylint: disable=C0103
WINDOWS_OS: Final[str] = "nt"
if os.name != WINDOWS_OS:
    import magic


logger = logging.getLogger(__name__)


# Allowed stream compressor formats for JSONL.
COMPRESSED_BZIP2 = "application/x-bzip2"
COMPRESSED_GZIP = "application/gzip"
COMPRESSED: Final[list] = [
    COMPRESSED_BZIP2,
    COMPRESSED_GZIP,
]


def _unpack_bz(path: str) -> Any:
    """Return bzip2 contents."""
    data = None
    with bz2.open(path, "rb") as bzip_file:
        data = bzip_file.read()
    return data


def _unpack_bz2(path: str) -> Any:
    """Alias for _unpack_bz."""
    return _unpack_bz(path)


def _unpack_gzip(path: str) -> Any:
    """Return gzip contents."""
    data = None
    with gzip.open(path, "rb") as gzip_file:
        data = gzip_file.read()
    return data


def _unpack_gz(path: str):
    """Alias for _unpack_gzip"""
    return _unpack_gzip(path)


async def compress_check(path):
    """If we're enabling detection of JSONL we need to be able to
    detect content in stream compressed files such as gzip or bzip2.
    python-magic (libmagic) does a good job enabling this for us.

    govdocs without libmagic:

        real	2m23.181s
        user	1m19.272s
        sys	    0m59.182s

    govdocs with:

        real	2m39.733s
        user	1m30.068s
        sys	    1m3.820s

    """
    if os.name == WINDOWS_OS:
        return False
    mime = magic.Magic(mime=True, uncompress=False)
    mime_type = mime.from_buffer(path)
    if mime_type not in COMPRESSED:
        return False
    logger.debug("compreessed mime detected: %s", mime_type)
    return mime_type


async def decompress_stream(path: str, compression: str) -> str:
    """Decomprerss our stream object and return the data."""
    if compression not in COMPRESSED:
        logger.error("invalid compression as input: %s", compression)
        return
    if compression == COMPRESSED_BZIP2:
        return _unpack_bz(path)
    if compression == COMPRESSED_GZIP:
        return _unpack_gzip(path)
