""" json-id tests... """

# pylint: disable=C0103

import json
from typing import Final

import pytest

from src.template.registry import IS_JSON, RegistryEntry, matcher

fundamentals_registry = [
    RegistryEntry(
        identifier="test_id1",
        name="test_1",
        version="1",
        markers=[{"test1": 1}, {"test2": "data"}],
    ),
    RegistryEntry(
        identifier="test_id2",
        name="test_2",
        version="1",
        markers=[{"test2": 1}, {"test3": {"test4": {"test5": None}}}],
    ),
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

fundamental_tests = [
    (fundamentals_registry, test_data_1, "test_id1"),
    (fundamentals_registry, test_data_2, "test_id2"),
]


@pytest.mark.parametrize("registry, test_data, expected_id", fundamental_tests)
def test_fundamentals(mocker, registry, test_data, expected_id):
    """Ensure the main function for the template repository exists."""
    mocker.patch("src.template.registry.registry", return_value=registry)
    try:
        json_loaded = json.loads(test_data)
    except json.JSONDecodeError as err:
        assert False, f"data won't decode as JSON: {err}"
    res = matcher(json_loaded)
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
    res = matcher(only_json)
    assert res[0].identifier == "id0"
    assert res[0].description == IS_JSON
