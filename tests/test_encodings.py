"""Test encodings as they are added to this utility."""

# pylint: disable=C0103

from typing import Final

import pytest

from src.jsonid import jsonid, registry

json_map: Final[str] = '{"a": "b"}\n'
json_list: Final[str] = "[]\n"
json_text: Final[str] = '"test"\n'
json_int: Final[str] = "123\n"
json_float: Final[str] = "1.11\n"
json_map_whitespace: Final[str] = '      \n\n\t\n{"a": "b"}\n'
json_list_whitespace: Final[str] = "      \n\n\t\n[]\n"
json_big5 = '{"\u5ee3\u5dde": "\u5ee3\u5dde"}\n'
json_shift_jis = '{"\u307d\u3063\u3077\u308b\u30e1\u30a4\u30eb": "\u307d\u3063\u3077\u308b\u30e1\u30a4\u30eb"}\n'


to_write: Final[dict] = {
    "map": json_map,
    "list": json_list,
    "int": json_int,
    "float": json_float,
    "map_whitespace": json_map_whitespace,
    "list_whitespace": json_list_whitespace,
    "big5": json_big5,
    "shift_jis": json_shift_jis,
}

encoding_tests = [
    ("UTF-8", to_write),
    ("UTF-16", to_write),
    ("UTF-16LE", to_write),
    ("UTF-16BE", to_write),
    ("UTF-32", to_write),
    ("UTF-32LE", to_write),
    ("UTF-32BE", to_write),
    ("BIG5", to_write),
    ("SHIFT-JIS", to_write),
]


@pytest.mark.parametrize("encoding, data_to_write", encoding_tests)
@pytest.mark.asyncio
async def test_encodings(tmp_path, encoding, data_to_write):
    """Test UTF-16 handling by mocking the BOM but then not providing
    any valid JSON data.
    """

    dir_ = tmp_path / "encodings"
    dir_.mkdir()
    for key, value in data_to_write.items():
        json_file = dir_ / f"{encoding}-{key}.json"
        json_file.open("w", encoding=encoding).write(value)
        res, data, _ = await jsonid.identify_plaintext_bytestream(json_file)
        assert res is True, f"{json_file} couldn't be opened with encoding"

        id_ = registry.matcher(data, encoding=encoding)
        print(value, id_)
        assert len(id_) > 0, f"{json_file} results list is incorrect: {len(id_)}"
        assert (
            id_[0].identifier == "jrid:0000"
        ), f"{json_file} couldn't be identified as JSON"
