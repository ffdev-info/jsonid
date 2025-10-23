"""Provide some integration testing to ensure consistency of reporting
outputs from the tool.
"""

import pytest

from src.jsonid import file_processing, jsonid

"""
        # TODO: for binary and empty files they may still need to
        # be output...
        #
        #  application/octet-stream; charset=binary
        #  inode/x-empty; charset=binary
        #  application/x-xz; charset=binary
        #  jsonl -- consider application/json
        #  application/json; charset=us-ascii
        #  application/jsonl+<suffix>
"""

integration_tests = [
    (
        # JSON example: {"test": "1"} .
        b"\x7b\x22\x74\x65\x73\x74\x22\x3a\x20\x22\x31\x22\x7d\x0a",
        'test_file.json: application/json; charset=UTF-8; doctype="JavaScript Object Notation (JSON)"; ref=jrid:TODO:JSON',
    ),
]


@pytest.mark.parametrize("data, expected", integration_tests)
@pytest.mark.asyncio
async def test_jsonl_processing(data, expected, capsys, tmp_path):
    """Ensure that JSONL processing worrks as expected."""
    test_file = tmp_path / "test_file.json"
    test_file.write_bytes(data)
    await file_processing.identify_json(
        [test_file], jsonid.decode_strategies, False, False
    )
    captured = capsys.readouterr()
    res = captured.out.strip()
    assert res == expected
