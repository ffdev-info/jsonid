"""JSONL requires some slightly special handling. Let's make sure
any exceptions to the rule work here.
"""

import bz2
import gzip
import sys

import pytest

from src.jsonid import compressionlib, file_processing, jsonid, registry

jsonl_1_valid = """
 1
 2
 3
"""
jsonl_2_valid = """
[1]
[2]
[3]
"""
jsonl_3_valid = """
{"hello": "world"}
{"world": "hello"}
"""
jsonl_4_invalid = ""
jsonl_5_single_line = "[1, 2, 3]"

jsonl_tests = [
    (jsonl_1_valid, True, registry.DOCTYPE_JSONL),
    (jsonl_2_valid, True, registry.DOCTYPE_JSONL),
    (jsonl_3_valid, True, registry.DOCTYPE_JSONL),
    (jsonl_4_invalid, False, False),
    (jsonl_5_single_line, True, registry.DOCTYPE_JSONL),
]


@pytest.mark.parametrize("content, validity, doctype", jsonl_tests)
def test_jsonl_processing(content, validity, doctype):
    """Ensure that JSONL processing worrks as expected."""
    valid, _, doctype_res = file_processing._jsonl_processing(content)
    assert valid == validity
    assert doctype_res == doctype


bz_tests = [
    (jsonl_1_valid, registry.DOCTYPE_JSONL, compressionlib.COMPRESSED_BZIP2),
    (jsonl_2_valid, registry.DOCTYPE_JSONL, compressionlib.COMPRESSED_BZIP2),
    (jsonl_3_valid, registry.DOCTYPE_JSONL, compressionlib.COMPRESSED_BZIP2),
    (jsonl_4_invalid, None, None),
    (jsonl_5_single_line, registry.DOCTYPE_JSON, compressionlib.COMPRESSED_BZIP2),
]


@pytest.mark.skipif(
    sys.platform.startswith("win"), reason="python-magic incompatibilties"
)
@pytest.mark.parametrize("content, doctype, compression", bz_tests)
@pytest.mark.asyncio
async def test_bz_jsonl(tmp_path, content, doctype, compression):
    """Make sure we can unpack bzip content and identify its base
    format.
    """
    test_dir = tmp_path / "jsonl_tests"
    test_dir.mkdir()
    bz = bz2.compress(content.encode())
    test_path = test_dir / "test_filename.jsonl.bz"
    test_path.write_bytes(bz)
    res = await file_processing.identify_plaintext_bytestream(
        test_path, jsonid.decode_strategies
    )
    assert res.doctype == doctype
    assert res.compression == compression


gz_tests = [
    (jsonl_1_valid, registry.DOCTYPE_JSONL, compressionlib.COMPRESSED_GZIP),
    (jsonl_2_valid, registry.DOCTYPE_JSONL, compressionlib.COMPRESSED_GZIP),
    (jsonl_3_valid, registry.DOCTYPE_JSONL, compressionlib.COMPRESSED_GZIP),
    (jsonl_4_invalid, None, None),
    (jsonl_5_single_line, registry.DOCTYPE_JSON, compressionlib.COMPRESSED_GZIP),
]


@pytest.mark.skipif(
    sys.platform.startswith("win"), reason="python-magic incompatibilties"
)
@pytest.mark.parametrize("content, doctype, compression", gz_tests)
@pytest.mark.asyncio
async def test_gz_jsonl(tmp_path, content, doctype, compression):
    """Make sure we can unpack gzip content and identify its base
    format.
    """
    test_dir = tmp_path / "jsonl_tests"
    test_dir.mkdir()
    test_path = test_dir / "test_filename.jsonl.gz"
    with gzip.open(test_path, "wb") as f:
        f.write(content.encode())
    res = await file_processing.identify_plaintext_bytestream(
        test_path, jsonid.decode_strategies
    )
    assert res.doctype == doctype
    assert res.compression == compression
