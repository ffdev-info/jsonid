""" json-id tests... """

# pylint: disable=C0103,R0401

import json
from typing import Final

import pytest

from src.jsonid import registry, registry_data

fundamentals_registry = [
    registry_data.RegistryEntry(
        identifier="test_id1",
        name="one key with integer, one key with string",
        version="1",
        markers=[{"KEY": "test1", "IS": 1}, {"KEY": "test2", "IS": "data"}],
    ),
    registry_data.RegistryEntry(
        identifier="test_id2",
        name="one key with integer one key with nested data",
        version="1",
        markers=[
            {"KEY": "test2", "IS": 1},
            {"KEY": "test3", "IS": {"test4": {"test5": None}}},
        ],
    ),
    registry_data.RegistryEntry(
        identifier="test_id3",
        name="key only identification (allows testing for only keys)",
        version="1",
        markers=[{"KEY": "@testkey", "EXISTS": None}],
    ),
    # Identical matches,
]

test_data_1: Final[
    str
] = """
    {
        "test1": 1,
        "test2": "data"
    }
    """

test_data_2: Final[
    str
] = """
        {
            "test2": 1,
            "test3": {
                "test4": {
                   "test5": null
                }
            }
        }
    """

test_data_3: Final[
    str
] = """
        {
            "@testkey": "ANYDATA",
            "key": "value"
        }
    """

fundamental_tests = [
    (fundamentals_registry, test_data_1, "test_id1"),
    (fundamentals_registry, test_data_2, "test_id2"),
    (fundamentals_registry, test_data_3, "test_id3"),
]


@pytest.mark.parametrize("test_registry, test_data, expected_id", fundamental_tests)
def test_fundamentals(mocker, test_registry, test_data, expected_id):
    """Test the foundational components of this identification tool."""
    mocker.patch("src.jsonid.registry_data.registry", return_value=test_registry)
    try:
        json_loaded = json.loads(test_data)
    except json.JSONDecodeError as err:
        assert False, f"data won't decode as JSON: {err}"
    res = registry.matcher(json_loaded)
    assert len(res) == 1, "results for these tests should have one value only"
    assert res[0].identifier == expected_id


def test_json_only():
    """Test that the result of an non identification for a valid
    JSON file is predictable.
    """
    only_json = """
        {
            "test1": 1,
            "test2": "data"
        }
        """
    try:
        json_loaded = json.loads(only_json)
    except json.JSONDecodeError as err:
        assert False, f"data won't decode as JSON: {err}"
    res = registry.matcher(json_loaded)
    assert res[0].identifier == "id0"
    assert res[0].description[0]["@en"] == registry.IS_JSON


primitive_tests = [
    ("[1,2,3]", registry.TYPE_LIST),
    ("[]", registry.TYPE_NONE),
    ("{}", registry.TYPE_NONE),
    ("null", registry.TYPE_NONE),
    ('{"k1": 1}', registry.TYPE_DICT),
    ('"true"', registry.TYPE_BOOL),
    ('"false"', registry.TYPE_BOOL),
    ("1.0", registry.TYPE_FLOAT),
    ("1", registry.TYPE_INT),
]


@pytest.mark.parametrize("test_data, expected_additional", primitive_tests)
def test_forms(test_data, expected_additional):
    """Test other JSON forms beyond object based JSON."""
    try:
        json_loaded = json.loads(test_data)
    except json.JSONDecodeError as err:
        assert False, f"data won't decode as JSON: {err}"
    res = registry.matcher(json_loaded)
    assert res[0].additional == expected_additional
