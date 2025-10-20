"""Test specific examples from the registry. """

# pylint: disable=C0103,R0801

import json
from dataclasses import dataclass

import pytest

from src.jsonid import analysis, file_processing, registry, registry_class


@dataclass
class base_obj_mock:
    """Mock base_obj object to enable testing."""

    data: str
    encoding: str
    doctype: str
    compression: str = None


specific_registry = [
    registry_class.RegistryEntry(
        identifier="id0019",
        name=[{"@en": "JSON Patch RFC 6902"}],
        markers=[
            {"INDEX": 0, "KEY": "op", "EXISTS": None},
            {"INDEX": 0, "KEY": "path", "EXISTS": None},
        ],
    ),
]

json_patch = """
   [
     { "op": "test", "path": "/a/b/c", "value": "foo" },
     { "op": "remove", "path": "/a/b/c" },
     { "op": "add", "path": "/a/b/c", "value": [ "foo", "bar" ] },
     { "op": "replace", "path": "/a/b/c", "value": 42 },
     { "op": "move", "from": "/a/b/c", "path": "/a/b/d" },
     { "op": "copy", "from": "/a/b/d", "path": "/a/b/e" }
   ]

"""


specific_tests = [
    (specific_registry, json_patch, "id0019"),
]


@pytest.mark.parametrize("test_registry, test_data, expected_id", specific_tests)
def test_specific(mocker, test_registry, test_data, expected_id):
    """Test specific examples that have been challenging."""
    mocker.patch("src.jsonid.registry_data.registry", return_value=test_registry)
    try:
        json_loaded = json.loads(test_data)
    except json.JSONDecodeError as err:
        assert False, f"data won't decode as JSON: {err}"
    base_obj = base_obj_mock(
        data=json_loaded,
        encoding="",
        doctype="json",
    )
    res = registry.matcher(base_obj=base_obj)
    assert res[0].identifier == expected_id


depth_test_1 = {
    "children": [
        {
            "name": "product service",
            "children": [
                {"name": "price", "children": [{"name": "cost", "size": 8}]},
                {"name": "quality", "children": [{"name": "messaging", "size": 4}]},
            ],
        },
        {
            "name": "customer service",
            "children": [
                {"name": "Personnel", "children": [{"name": "CEO", "size": 7}]}
            ],
        },
        {
            "name": "product",
            "children": [
                {"name": "Apple", "children": [{"name": "iPhone 4", "size": 10}]}
            ],
        },
    ]
}


specific_tests = [
    (depth_test_1, 7),
]


@pytest.mark.parametrize("depth_test, expected_depth", specific_tests)
def test_get_depth(depth_test, expected_depth):
    """Assert depth tests work."""
    assert analysis.analyse_depth(depth_test) == expected_depth


@pytest.mark.asyncio
async def test_utf16(tmp_path):
    """Test UTF-16 handling by mocking the BOM but then not providing
    any valid JSON data.
    """

    json_data = '{"a": "b"}'
    dir_ = tmp_path / "jsonid-utf16"
    dir_.mkdir()
    file_ = dir_ / "utftest.json"
    file_.write_text(json_data, encoding="utf-16")
    base_obj = await file_processing.identify_plaintext_bytestream(
        file_,
        strategy=["JSON"],
    )
    assert base_obj == registry.BaseCharacteristics(
        valid=True,
        data={"a": "b"},
        doctype=registry.DOCTYPE_JSON,
        encoding="UTF-16",
        text=True,
    )
    json_data = '{"a": "b"'
    dir_ = tmp_path / "jsonid-utf16-broken"
    dir_.mkdir()
    file_ = dir_ / "utftest.json"
    file_.write_text(json_data, encoding="utf-16")
    base_obj = await file_processing.identify_plaintext_bytestream(
        file_,
        strategy=["JSON"],
    )
    assert base_obj == registry.BaseCharacteristics(
        valid=False,
        binary=False,
        text=True,
    )

    json_data = '{"a": "b"}'
    dir_ = tmp_path / "jsonid-utf16LE"
    dir_.mkdir()
    file_ = dir_ / "utftest.json"
    file_.write_text(json_data, encoding="UTF-16LE")
    base_obj = await file_processing.identify_plaintext_bytestream(
        file_,
        strategy=["JSON"],
    )
    assert base_obj == registry.BaseCharacteristics(
        valid=True,
        data={"a": "b"},
        doctype=registry.DOCTYPE_JSON,
        encoding="UTF-16",
        binary=False,
        text=True,
    )  # apparently this is equivalent to plain UTF-16.

    json_data = '{"a": "b"}'
    dir_ = tmp_path / "jsonid-utf16BE"
    dir_.mkdir()
    file_ = dir_ / "utftest.json"
    file_.write_text(json_data, encoding="UTF-16BE")
    base_obj = await file_processing.identify_plaintext_bytestream(
        file_,
        strategy=["JSON"],
    )
    assert base_obj == registry.BaseCharacteristics(
        valid=True,
        data={"a": "b"},
        doctype=registry.DOCTYPE_JSON,
        encoding="UTF-16BE",
        text=True,
        binary=False,
    )


@pytest.mark.asyncio
async def test_text_check():
    """Make sure the text check works"""
    assert await file_processing.text_check("\x7f".encode()) is False
    assert await file_processing.text_check("\x03".encode()) is False
    assert await file_processing.text_check("\x50\x4b\x03\x04".encode()) is False
    assert await file_processing.text_check("\x50\x4b\x03".encode()) is False
    assert await file_processing.text_check("\x01".encode()) is False
    assert await file_processing.text_check("\x2d".encode()) is True
    assert await file_processing.text_check("📚".encode()) is True
    assert await file_processing.text_check("---".encode()) is True
    assert await file_processing.text_check("{".encode()) is True
    assert await file_processing.text_check("   \n".encode()) is True
