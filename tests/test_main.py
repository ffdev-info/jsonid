""" json-id tests... """

# pylint: disable=C0103

import json
from typing import Final

import pytest

from src.template.registry import RegistryEntry, matcher

fundamentals_registry = [
    RegistryEntry(
        identifier="id1",
        name="test_1",
        version="1",
        markers={"test1": 1, "test2": "data"},
    )
]

test_data_1: Final[
    str
] = """
    {
        "test1": 1,
        "test2": "data"
    }
    """

fundamental_tests = [
    (fundamentals_registry, test_data_1, "id1"),
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
    assert res[0].identifier == expected_id
