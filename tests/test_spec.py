"""Some basic tests to make sure the spec is working."""

# pylint: disable=C0103

import json
from typing import Final

import pytest

from src.template.registry import IS_JSON, RegistryEntry, matcher


spec_registry = [
    RegistryEntry(
        identifier="contains1",
        name="spec: contains",
        version="1",
        markers=[
            {"KEY": "k1", "CONTAINS": "xyx"},
        ],
    ),
    RegistryEntry(
        identifier="startswith1",
        name="spec: starts with",
        version="1",
        markers=[
            {"KEY": "k1", "STARTSWITH": "xyx"},
        ],
    ),
    RegistryEntry(
        identifier="endswith1",
        name="spec: endswith",
        version="1",
        markers=[
            {"KEY": "k1", "ENDSWITH": "xyx"},
        ],
    ),
    RegistryEntry(
        identifier="is1",
        name="spec: is",
        version="1",
        markers=[
            {"KEY": "k1", "IS": "xyx"},
        ],
    ),
    RegistryEntry(
        identifier="regex1",
        name="spec: regex",
        version="1",
        markers=[
            {"KEY": "k1", "REGEX": "(\d+)(xyz)(\d{3}[a-z]+)"},
        ],
    ),
    RegistryEntry(
        identifier="exists1",
        name="spec: exists",
        version="1",
        markers=[
            {"KEY": "k1", "EXISTS": None},
        ],
    ),
]

contains_1: Final[
    str
] = """
    {
        "k1": "somedata xyz more data"
    }
    """

startswith_1: Final[
    str
] = """
        {
            "k1": "xyz more data"
        }
    """
endswith_1: Final[str] = """
        {
            "k1": "more data xyz"
        }
"""

is_1: Final[str] = """
        {
            "k1": "xyz"
        }
"""

regex_1: Final[str] = """
        {
            "k1": "12345xyz567abcdef"
        }
"""

exists_1: Final[str] = """
        {
            "k1": null
        }
"""

spec_tests = [
    (spec_registry, contains_1, "contains1"),
    (spec_registry, startswith_1, "startswith1"),
    (spec_registry, endswith_1, "endswith1"),
    (spec_registry, is_1, "is1"),
    (spec_registry, regex_1, "regex1"),
    (spec_registry, exists_1, "exists1"),
]


@pytest.mark.parametrize("registry, test_data, expected_id", spec_tests)
def test_spec(mocker, registry, test_data, expected_id):
    """Ensure the main function for the template repository exists."""
    print("test:", expected_id)
    mocker.patch("src.template.registry.registry", return_value=registry)
    try:
        json_loaded = json.loads(test_data)
    except json.JSONDecodeError as err:
        assert False, f"data won't decode as JSON: {err}"
