"""Provide some integration testing to ensure consistency of reporting
outputs from the tool.
"""

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



import pytest

from src.jsonid import file_processing, jsonid

integration_tests = [
    (
        '{"test": "1"}',
        'test_file.json: application/json; charset=UTF-8; doctype="JavaScript Object Notation (JSON)"; ref=jrid:TODO:JSON',
    ),
]


@pytest.mark.parametrize("data, expected", integration_tests)
@pytest.mark.asyncio
async def test_jsonl_processing(data, expected, capsys, tmp_path):
    """Ensure that JSONL processing worrks as expected."""
    test_file = tmp_path / "test_file.json"
    test_file.write_text(data, encoding="UTF-8")
    await file_processing.identify_json(
        [test_file], jsonid.decode_strategies, False, False
    )
    captured = capsys.readouterr()
    res = captured.out.strip()
    assert res == expected
