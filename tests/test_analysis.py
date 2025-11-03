"""Test analysis output."""

# pylint: disable=C0103

import json
import tomllib as toml
from typing import Final

import pytest
import yaml

from src.jsonid import analysis

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

example_1: Final[dict] = {}
example_2: Final[list] = []
example_3: Final[list] = [1, 2, "", None, 1.2, "❤💖💙💚💛💜💝", "♕♖♗♘♙♚♛♜♝♞♟"]
example_4: Final[dict] = {"key1": "value", "key2": "value", "key3": "value"}
example_5: Final[list] = [[[]]]

# Spec examples: https://raw.githubusercontent.com/IQSS/UNF/master/doc/unf_examples.txt
spec_example_6: Final[float] = 3.1415
spec_example_7: Final[str] = False
spec_example_8: Final[str] = ""

ex4_equivalent_1: Final[dict] = {"key2": "value", "key1": "value", "key3": "value"}
ex4_equivalent_2: Final[dict] = {"key3": "value", "key2": "value", "key1": "value"}

unf_simple_tests: Final[list] = [
    (example_1, "UNF:6:i6V/mh1/7flCe+qLZ7Jn2A==", []),
    (example_2, "UNF:6:47DEQpj8HBSa+/TImW+5JA==", []),
    (example_3, "UNF:6:d1QWNdwYIhjx0pONjMCE8w==", []),
    (example_4, "UNF:6:4Kq/xUBxuJTR+B1NaNPxNg==", [ex4_equivalent_1, ex4_equivalent_2]),
    (example_5, "UNF:6:KoUoJgCjaWBHjlDkcWpq4A==", []),
    (spec_example_6, "UNF:6:vOSZmXXXpKfQcqZ0Cuu5/w==", []),
    (spec_example_7, "UNF:6:YUvj33xEHnzirIHQyZaHow==", []),
    (spec_example_8, "UNF:6:ECtRuXZaVqPomffPDuOOUg==", []),
]


@pytest.mark.parametrize("example, expected, equivalents", unf_simple_tests)
@pytest.mark.asyncio
async def test_unf_fingerprint(example, expected, equivalents):
    """Test the UNF fingerprint method."""
    res = await analysis.unf_fingerprint(example)
    assert res == expected
    for item in equivalents:
        equivalent_res = await analysis.unf_fingerprint(item)
        assert equivalent_res == res


cid_simple_tests = [
    (example_1, "bafkreifyuqjaicfhnyzvgfw6tigbheur3jst5l72xhfribv4z5qvud7usu", []),
    (example_2, "bafkreifbc4uincfnle4i6melqkvda5k3zvt5mrqwevjb24fefqizclomau", []),
    (example_3, "bafkreieb4f2p6eqldcydwhsxnf6zmnprswhfzh6zdhwgkp6ka6oxq65rxi", []),
    (
        example_4,
        "bafkreibgwpsvtv2xwvdlqk66kmgob6pjiawaa437rqnpp4h27u433kjy4q",
        [ex4_equivalent_1, ex4_equivalent_2],
    ),
    (example_5, "bafkreidn5i3rkmeyrywbkuxuelps5vcor3khednockgqwwpswmkkmq6rtm", []),
]


@pytest.mark.parametrize("example, expected, equivalents", cid_simple_tests)
@pytest.mark.asyncio
async def test_cid_fingerprint(example, expected, equivalents):
    """Test the IPLD fingerprint method."""
    res = await analysis.ipld_cid(example)
    assert res == expected
    for item in equivalents:
        equivalent_res = await analysis.ipld_cid(item)
        assert equivalent_res == res


depth_1: Final[list] = {"key1": []}

# Depth == 8. The last array is empty and has no depth. Contrast this
# with the other arrays which contain at least one array.
depth_2: Final[int] = {
    "key1": [[[[[]]]]],
    "key2": {"key3": {"key4": 1}},
    "key5": [],
    "key6": [[[[[[[[]]]]]]]],
}

# Depth == 4.
depth_3: Final[dict] = {"key1": {"key2": {"key3": {"key4": 1}}}}

# Depth == 4. The last array is empty and so has no depth. Contrast this
# with the other arrays which contain at least one array.
depth_4: Final[dict] = {"key1": [[[]]]}

depth_5: Final[list] = [[[[]]]]

depth_6: Final[float] = 3.1415

depth_7: Final[int] = 1

# Depth == 6.
depth_8: Final[dict] = {
    "key1": {"key2": {"key3": {"key4": {"key5": 1}}}},
    "key2": {"key2": {"key3": {"key4": {"key5": {"key6": 1}}}}},
    "key3": {"key2": {"key3": {"key4": {"key5": 1}}}},
    "key4": {"key2": {"key3": 1}},
}

depth_9: Final[list] = [[[[[1]]]], [[[[1]]]], [[[[1]]]], [[1]]]

# Depth == 7.
depth_10: Final[dict] = {
    "key1": {"key2": 1},
    "key2": [1, 2, {"key3": [1, 2, 3, {"key4": [1, {"key5": 2}]}]}],
}

# Map is empty.
depth_11: Final[dict] = {}

# Array is empty.
depth_12: Final[dict] = []

# Array contains one item.
depth_13: Final[dict] = [[]]

# Map contains one item.
depth_14: Final[dict] = {"key1": None}

depth_tests: Final[list] = [
    (depth_1, 1),
    (depth_2, 8),
    (depth_3, 4),
    (depth_4, 3),
    (depth_5, 3),
    (depth_6, 0),
    (depth_7, 0),
    (depth_8, 6),
    (depth_9, 5),
    (depth_10, 7),
    (depth_11, 0),
    (depth_12, 0),
    (depth_13, 1),
    (depth_14, 1),
]


@pytest.mark.parametrize("example, expected", depth_tests)
@pytest.mark.asyncio
async def test_analyse_depth(example, expected):
    """Test depth analysis."""
    depth = analysis.analyse_depth(example)
    assert depth == expected


complex_1: Final[dict] = {"key1": [1, 2, "three"]}

complex_2: Final[dict] = {"key1": [1, 2, 3]}

complex_3: Final[dict] = {"key1": {"key2": [1, 2, "three"]}}


complex_4: Final[dict] = {
    "key1": {"key2": [1, 2, 3]},
    "key2": {"key3": [1, 2, "three"]},
}

complex_5: Final[dict] = {"key1": {"key2": [1, 2, 3]}, "key2": {"key3": [1, 2, 3]}}

complex_6: Final[list] = [[[[[1]]]], [[[[1]]]], [[[[1]]]], [[1]]]

complex_7: Final[list] = [[[[[1, 1.2]]]], [[[[1]]]], [[[[1]]]], [[1]]]

complex_8: Final[list] = [[[[[1, 2, 3]]]], [[[[1]]]], [[[[1, "two"]]]], [[1]]]

complex_9: Final[dict] = {
    "key1": {"key2": [1, 2, 3]},
    "key2": {"key3": {"key4": {"key5": [1, 2, "three"]}}},
}

complex_10: Final[dict] = {
    "key1": {"key2": [1, 2, 3]},
    "key2": {"key2": [1, 2, 3]},
}

complex_11: Final[float] = 3.1415

complex_12: Final[int] = 1
complex_13: Final[int] = 1000

complex_14: Final[dict] = {
    "key1": {"key2": 1},
    "key2": [1, 2, {"key3": [1, 2, 3, {"key4": [1, {"key5": 2}]}]}],
}

complex_tests: Final[list] = [
    (complex_1, True),
    (complex_2, False),
    (complex_3, True),
    (complex_4, True),
    (complex_5, False),
    (complex_6, False),
    (complex_7, True),
    (complex_8, True),
    (complex_9, True),
    (complex_10, False),
    (complex_11, False),
    (complex_12, False),
    (complex_13, False),
    (complex_14, True),
]


@pytest.mark.parametrize("example, expected", complex_tests)
@pytest.mark.asyncio
async def test_analyse_list_types(example, expected):
    """Test the list types analysis."""
    complex_types = await analysis.analyse_list_types(example)
    assert complex_types == expected


top_level_1: Final[dict] = {
    "key1": {"key2": 1},
    "key2": [1, 2, {"key3": [1, 2, 3, {"key4": [1, {"key5": 2}]}]}],
}

top_level_2 = top_level_1
top_level_3: Final[float] = 3.1415

top_level_res_1: Final[dict] = [
    "map",
    ["integer"],
    "list",
    [
        "integer",
        "integer",
        "map",
        [
            "list",
            [
                "integer",
                "integer",
                "integer",
                "map",
                ["list", ["integer", "map", ["integer"]]],
            ],
        ],
    ],
]


top_level_res_2: Final[dict] = [
    "map",
    "list",
]

top_level_res_3: Final[list] = [
    "float",
]


top_level_tests: Final[list] = [
    (top_level_1, top_level_res_1, True),
    (top_level_2, top_level_res_2, False),
    (top_level_3, top_level_res_3, False),
]


@pytest.mark.parametrize("example, expected, depth_all", top_level_tests)
@pytest.mark.asyncio
async def test_top_level_types(example, expected, depth_all):
    """Test the types analysis."""
    res = await analysis.analyse_all_types(example, depth_all)
    assert res == expected


integration_1: Final[dict] = {}
integration_2: Final[float] = 3.1415
integration_3: Final[int] = 1
integration_4: Final[list] = []
integration_5: Final[list] = ""

integration_content_1: Final[str] = "{}"
integration_content_2: Final[str] = "3.1415"
integration_content_3: Final[str] = "1"
integration_content_4: Final[str] = "[]"
integration_content_5: Final[str] = ""

integration_tests = [
    (integration_1, integration_content_1),
    (integration_2, integration_content_2),
    (integration_3, integration_content_3),
    (integration_4, integration_content_4),
    (integration_5, integration_content_5),
]


@pytest.mark.parametrize("data, content", integration_tests)
@pytest.mark.asyncio
async def test_analysis_partial_integration(data, content):
    """Perform a partial integration test to make sure output is
    as expected in exceptional cases.
    """
    res = await analysis.analyse_input(data, content, False)
    try:
        json.dumps(res)
    except Exception as err:  # pylint: disable=W0718
        assert False, f"JSON dumps should work for analysis: {err}"


roundtrip_tests = [
    (
        """
{
    "hello": "world",
    "goodbye": false,
    "values": [
        1,
        2,
        3.142
    ]
}

        """,
        """
values:
- 1
- 2
- 3.142
hello: world
goodbye: false
        """,
        """
values = [1, 2, 3.142]
hello = "world"
goodbye = false
        """,
        "UNF:6:97EfAWBIQlObVCVwa7kc0g==",
        "bafkreiawsimwdn4blnb7scz2cfwtdksifrayccsl3z6gmxam6uxddctkoy",
    )
]


@pytest.mark.parametrize("json_data, yaml_data, toml_data, UNF, CID", roundtrip_tests)
@pytest.mark.asyncio
async def test_equivalent_formats(
    json_data: str, yaml_data: str, toml_data: str, UNF: str, CID: str
):
    """Provide a mechanism for testing equivalencies."""

    res_json = await analysis.analyse_input(json.loads(json_data), "", False)
    res_yaml = await analysis.analyse_input(
        yaml.load(yaml_data.strip(), Loader=Loader), "", False
    )
    res_toml = await analysis.analyse_input(toml.loads(toml_data), "", False)

    assert res_json["fingerprint"] == res_yaml["fingerprint"] == res_toml["fingerprint"]
    assert res_json["fingerprint"]["unf"] == UNF
    assert res_json["fingerprint"]["cid"] == CID
