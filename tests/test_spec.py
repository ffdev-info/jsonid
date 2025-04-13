"""Some basic tests to make sure the spec is working."""

# pylint: disable=C0103

import json
from typing import Final

import pytest

from src.jsonid.registry import matcher
from src.jsonid.registry_data import RegistryEntry

spec_registry = [
    RegistryEntry(
        identifier="contains1",
        name="spec: contains",
        version="1",
        markers=[
            {"KEY": "k1", "CONTAINS": "CONTAINSxyzCONTAINS"},
        ],
    ),
    RegistryEntry(
        identifier="startswith1",
        name="spec: starts with",
        version="1",
        markers=[
            {"KEY": "k1", "STARTSWITH": "xyz"},
        ],
    ),
    RegistryEntry(
        identifier="endswith1",
        name="spec: endswith",
        version="1",
        markers=[
            {"KEY": "k1", "ENDSWITH": "xyz"},
        ],
    ),
    RegistryEntry(
        identifier="is1",
        name="spec: is",
        version="1",
        markers=[
            {"KEY": "k1", "IS": "ISxyzIS"},
        ],
    ),
    RegistryEntry(
        identifier="regex1",
        name="spec: regex",
        version="1",
        markers=[
            {"KEY": "k1", "REGEX": "(\\d+)(REGEX)(\\d{3}[a-z]+)"},
        ],
    ),
    RegistryEntry(
        identifier="exists1",
        name="spec: exists",
        version="1",
        markers=[
            {"KEY": "k1_exists", "EXISTS": None},
        ],
    ),
    RegistryEntry(
        identifier="index1",
        name="spec: index",
        version="1",
        markers=[
            {"INDEX": 0, "KEY": "k1_index", "EXISTS": None},
        ],
    ),
    RegistryEntry(
        identifier="goto1",
        name="spec: goto",
        version="1",
        markers=[
            {"GOTO": "k1_goto", "KEY": "k1_goto_1", "EXISTS": None},
        ],
    ),
    RegistryEntry(
        identifier="istype1",
        name="spec: istype",
        version="1",
        markers=[
            {"KEY": "k1_istype", "ISTYPE": int},
        ],
    ),
]

contains_1: Final[
    str
] = """
    {
        "k1": "somedata CONTAINSxyzCONTAINS more data"
    }
    """

startswith_1: Final[
    str
] = """
        {
            "k1": "xyz more data"
        }
    """
endswith_1: Final[
    str
] = """
        {
            "k1": "more data xyz"
        }
"""

is_1: Final[
    str
] = """
        {
            "k1": "ISxyzIS"
        }
"""

regex_1: Final[
    str
] = """
        {
            "k1": "12345REGEX567abcdef"
        }
"""

exists_1: Final[
    str
] = """
        {
            "k1_exists": null
        }
"""

noexist_1: Final[
    str
] = """
        {
            "k1_noexist": null
        }
"""

index_1: Final[
    str
] = """
[
    {
        "k1_index": null
    }
]
"""

goto_1: Final[
    str
] = """
{
    "k1_goto": {
        "k1_goto_1": null
    }
}
"""

istype_1: Final[
    str
] = """
{
    "k1_istype": 1
}
"""

spec_tests = [
    (spec_registry, contains_1, "contains1"),
    (spec_registry, startswith_1, "startswith1"),
    (spec_registry, endswith_1, "endswith1"),
    (spec_registry, is_1, "is1"),
    (spec_registry, regex_1, "regex1"),
    (spec_registry, exists_1, "exists1"),
    (spec_registry, index_1, "index1"),
    (spec_registry, goto_1, "goto1"),
    (spec_registry, istype_1, "istype1"),
]


@pytest.mark.parametrize("registry, test_data, expected_id", spec_tests)
def test_spec(mocker, registry, test_data, expected_id):
    """Test all keywords."""
    print("test:", expected_id)
    mocker.patch("src.jsonid.registry_data.registry", return_value=registry)
    try:
        json_loaded = json.loads(test_data)
    except json.JSONDecodeError as err:
        assert False, f"data won't decode as JSON: {err}"
    res = matcher(json_loaded)
    assert (
        len(res) == 1
    ), f"results for these tests should have one value only, got: {len(res)}"
    assert res[0].identifier == expected_id


no_exist_registry = [
    RegistryEntry(
        identifier="noexist1",
        name="spec: exists",
        version="1",
        markers=[
            {"KEY": "k1_not_exists", "NOEXIST": None},
        ],
    ),
]

noexist_1: Final[
    str
] = """
        {
            "k1_noexist": null
        }
"""


no_exist_registry = [
    (spec_registry, noexist_1, "noexist1"),
]


@pytest.mark.parametrize("registry, test_data, expected_id", spec_tests)
def test_noexist_spec(mocker, registry, test_data, expected_id):
    """Test the no-exist keyword."""
    print("test:", expected_id)
    mocker.patch("src.jsonid.registry_data.registry", return_value=registry)
    try:
        json_loaded = json.loads(test_data)
    except json.JSONDecodeError as err:
        assert False, f"data won't decode as JSON: {err}"
    res = matcher(json_loaded)
    assert (
        len(res) == 1
    ), f"results for these tests should have one value only, got: {len(res)}"
    assert res[0].identifier == expected_id
