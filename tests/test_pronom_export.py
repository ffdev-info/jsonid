"""Test PRONOM export functions.

NB. many of the tests here can be paramettrized once we have good
coverage. They've all been tested individually as the conversion
scripts are ironed out. This will take on more relevance if the
tool is used more for JSON signature creation in general.
"""

import pytest

from src.jsonid import pronom

encode_roundtrip_tests = [
    (
        "74657374",
        "7400650073007400",
        "utf-16",
    )
]


@pytest.mark.parametrize("hex_sequences, expected, encoding", encode_roundtrip_tests)
def test_encode_roundtrip(hex_sequences, expected, encoding):
    """Re-encode a set of hexadecimal values to a new encoding."""

    res = pronom.encode_roundtrip(hex_sequences, encoding)
    assert res == expected


preprocess_goto_tests = [
    (
        [
            {"KEY": "sops", "EXISTS": None},
            {"GOTO": "sops", "KEY": "kms", "EXISTS": None},
            {"GOTO": "sops", "KEY": "pgp", "EXISTS": None},
        ],
        [
            {"KEY": "sops", "EXISTS": None},
            {"KEY": "kms", "EXISTS": None},
            {"KEY": "pgp", "EXISTS": None},
        ],
    )
]


@pytest.mark.parametrize("markers_in, markers_out", preprocess_goto_tests)
def test_preprocess_goto_markers(markers_in: list, markers_out: list):
    """Make sure preprocess markers works as anticipated.

    GOTO is also largely synonymous with "KEY" exists and so we can
    remove duplicate examples of GOTO and ensure just one "EXISTS" for
    that GOTO exists.
    """

    res = pronom.preprocess_goto_markers(markers_in)
    assert res == markers_out


preprocess_index_tests = [
    (
        [
            {"INDEX": 0, "KEY": "Content-Length", "EXISTS": None},
            {"INDEX": 0, "KEY": "Content-Type", "EXISTS": None},
            {"INDEX": 0, "KEY": "X-TIKA:Parsed-By", "EXISTS": None},
            {"INDEX": 0, "KEY": "X-TIKA:parse_time_millis", "EXISTS": None},
        ],
        [
            {"INDEX_START": None},
            {"KEY": "Content-Length", "EXISTS": None},
            {"INDEX END": None},
            {"INDEX_START": None},
            {"KEY": "Content-Type", "EXISTS": None},
            {"INDEX END": None},
            {"INDEX_START": None},
            {"KEY": "X-TIKA:Parsed-By", "EXISTS": None},
            {"INDEX END": None},
            {"INDEX_START": None},
            {"KEY": "X-TIKA:parse_time_millis", "EXISTS": None},
            {"INDEX END": None},
        ],
    )
]


def test_export_sops():
    """SOPS is a good example of a more complex signature. Ensure
    it works here.
    """

    markers = [
        {"KEY": "sops", "EXISTS": None},
        {"GOTO": "sops", "KEY": "kms", "EXISTS": None},
        {"GOTO": "sops", "KEY": "pgp", "EXISTS": None},
    ]

    processed = pronom.process_markers(markers, 0, "utf-8")

    res = []
    for sequence in processed[0].byte_sequences:
        res.append(sequence.value)

    expected = [
        "7B",
        "22736F707322{0-16}3A",
        "226B6D7322{0-16}3A",
        "2270677022{0-16}3A",
        "7D",
    ]

    assert res == expected


def test_ocfl_inventory():
    """OFCL inventoty is one of the first examples that worked out of
    the box and provides good control for errors."""

    markers = [
        {"KEY": "type", "STARTSWITH": "https://ocfl.io/"},
        {"KEY": "type", "CONTAINS": "spec/#inventory"},
        {"KEY": "head", "EXISTS": None},
        {"KEY": "manifest", "EXISTS": None},
    ]

    processed = pronom.process_markers(markers, 0, "utf-8")

    res = []
    for sequence in processed[0].byte_sequences:
        res.append(sequence.value)

    expected = [
        "7B",
        "227479706522{0-16}3A{0-16}2268747470733A2F2F6F63666C2E696F2F",
        "227479706522{0-16}3A{0-16}22*737065632F23696E76656E746F7279*22",
        "226865616422{0-16}3A",
        "226D616E696665737422{0-16}3A",
        "7D",
    ]
    assert res == expected


def test_json_patch():
    """Ensure that JSON patch style markers are converted
    correctly.
    """

    markers = [
        {"INDEX": 0, "KEY": "op", "EXISTS": None},
        {"INDEX": 0, "KEY": "path", "EXISTS": None},
    ]

    processed = pronom.process_markers(markers, 0, "utf-8")

    res = []
    for sequence in processed[0].byte_sequences:
        res.append(sequence.value)

    expected = [
        "7B",
        "{0-16}5B*7B*226F7022{0-16}3A*7D*5D",
        "{0-16}5B*7B*227061746822{0-16}3A*7D*5D",
        "7D",
    ]

    assert res == expected


def test_gltf_schema():
    """Ensure that GLTF style patterns are converted correctly.

    NB. the pattern here is potentially different from that in the
    registry and the registry may need updating to be more
    permissive, or simply corrected.
    """

    markers = [
        {"KEY": "$schema", "STARTSWITH": "https://json-schema.org/"},
        {"KEY": "$schema", "ENDSWITH": "/schema"},
        {"KEY": "title", "EXISTS": None},
        {"KEY": "type", "IS": "object"},
        {"KEY": "description", "IS": "The root object for a glTF asset."},
    ]

    processed = pronom.process_markers(markers, 0, "utf-8")

    res = []
    for sequence in processed[0].byte_sequences:
        res.append(sequence.value)

    expected = [
        "7B",
        "2224736368656D6122{0-16}3A{0-16}2268747470733A2F2F6A736F6E2D736368656D612E6F72672F",
        "2224736368656D6122{0-16}3A{0-16}*2F736368656D6122",
        "227469746C6522{0-16}3A",
        "227479706522{0-16}6F626A656374",
        "226465736372697074696F6E22{0-16}54686520726F6F74206F626A65637420666F72206120676C54462061737365742E",
        "7D",
    ]

    assert res == expected


def test_tika_recursive():
    """Ensure that TIKA style signatures (relying largely on INDEX) are
    converted correctly.
    """

    markers = [
        {"INDEX": 0, "KEY": "Content-Length", "EXISTS": None},
        {"INDEX": 0, "KEY": "Content-Type", "EXISTS": None},
        {"INDEX": 0, "KEY": "X-TIKA:Parsed-By", "EXISTS": None},
        {"INDEX": 0, "KEY": "X-TIKA:parse_time_millis", "EXISTS": None},
    ]

    processed = pronom.process_markers(markers, 0, "utf-8")

    res = []
    for sequence in processed[0].byte_sequences:
        res.append(sequence.value)

    expected = [
        "7B",
        "{0-16}5B*7B*22436F6E74656E742D4C656E67746822{0-16}3A*7D*5D",
        "{0-16}5B*7B*22436F6E74656E742D5479706522{0-16}3A*7D*5D",
        "{0-16}5B*7B*22582D54494B413A5061727365642D427922{0-16}3A*7D*5D",
        "{0-16}5B*7B*22582D54494B413A70617273655F74696D655F6D696C6C697322{0-16}3A*7D*5D",
        "7D",
    ]

    assert res == expected


encoding_tests = [
    (
        [
            {"KEY": "test", "IS": "data"},
            {"KEY": "file", "ISTYPE": int},
            {"KEY": "bool", "ISTYPE": bool},
            {"KEY": "here", "EXISTS": None},
            {"KEY": "within", "CONTAINS": "value"},
            {"KEY": "start", "STARTSWITH": "value"},
            {"KEY": "end", "ENDSWITH": "value"},
            {"GOTO": "key", "KEY": "at", "EXISTS": None},
        ],
        [
            "7B",
            "227465737422{0-16}64617461",
            "2266696C6522{0-16}3A{0-16}[30:39]",
            "22626F6F6C22{0-16}3A{0-16}(74727565|66616C7365)",
            "226865726522{0-16}3A",
            "2277697468696E22{0-16}3A{0-16}22*76616C7565*22",
            "22737461727422{0-16}3A{0-16}2276616C7565",
            "22656E6422{0-16}3A{0-16}*76616C756522",
            "226B657922{0-16}3A",
            "22617422{0-16}3A",
            "7D",
        ],
        "utf-8",
    ),
    (
        [
            {"INDEX": 1, "KEY": "key", "EXISTS": None},
        ],
        [
            "7B",
            "{0-16}5B*7B*226B657922{0-16}3A*7D*5D",
            "7D",
        ],
        "utf-8",
    ),
    (
        [
            {"KEY": "test", "IS": "data"},
            {"KEY": "file", "ISTYPE": int},
            {"KEY": "bool", "ISTYPE": bool},
            {"KEY": "here", "EXISTS": None},
            {"KEY": "within", "CONTAINS": "value"},
            {"KEY": "start", "STARTSWITH": "value"},
            {"KEY": "end", "ENDSWITH": "value"},
            {"GOTO": "key", "KEY": "at", "EXISTS": None},
        ],
        [
            "7B00",
            "220074006500730074002200{0-16}6400610074006100",
            "2200660069006C0065002200{0-16}3A00{0-16}[30:39]",
            "220062006F006F006C002200{0-16}3A00{0-16}(7400720075006500|660061006C0073006500)",
            "220068006500720065002200{0-16}3A00",
            "2200770069007400680069006E002200{0-16}3A00{0-16}2200*760061006C0075006500*2200",
            "2200730074006100720074002200{0-16}3A00{0-16}2200760061006C0075006500",
            "220065006E0064002200{0-16}3A00{0-16}*760061006C00750065002200",
            "22006B00650079002200{0-16}3A00",
            "2200610074002200{0-16}3A00",
            "7D00",
        ],
        "utf-16",
    ),
    (
        [
            {"INDEX": 1, "KEY": "key", "EXISTS": None},
        ],
        [
            "7B00",
            "{0-16}5B00*7B00*22006B00650079002200{0-16}3A00*7D00*5D00",
            "7D00",
        ],
        "utf-16",
    ),
    (
        [
            {"KEY": "test", "IS": "data"},
            {"KEY": "file", "ISTYPE": int},
            {"KEY": "bool", "ISTYPE": bool},
            {"KEY": "here", "EXISTS": None},
            {"KEY": "within", "CONTAINS": "value"},
            {"KEY": "start", "STARTSWITH": "value"},
            {"KEY": "end", "ENDSWITH": "value"},
            {"GOTO": "key", "KEY": "at", "EXISTS": None},
        ],
        [
            "007B",
            "002200740065007300740022{0-16}0064006100740061",
            "002200660069006C00650022{0-16}003A{0-16}[30:39]",
            "00220062006F006F006C0022{0-16}003A{0-16}(0074007200750065|00660061006C00730065)",
            "002200680065007200650022{0-16}003A",
            "002200770069007400680069006E0022{0-16}003A{0-16}0022*00760061006C00750065*0022",
            "0022007300740061007200740022{0-16}003A{0-16}002200760061006C00750065",
            "00220065006E00640022{0-16}003A{0-16}*00760061006C007500650022",
            "0022006B006500790022{0-16}003A",
            "0022006100740022{0-16}003A",
            "007D",
        ],
        "utf-16BE",
    ),
    (
        [
            {"INDEX": 1, "KEY": "key", "EXISTS": None},
        ],
        [
            "007B",
            "{0-16}005B*007B*0022006B006500790022{0-16}003A*007D*005D",
            "007D",
        ],
        "utf-16BE",
    ),
    (
        [
            {"KEY": "test", "IS": "data"},
            {"KEY": "file", "ISTYPE": int},
            {"KEY": "bool", "ISTYPE": bool},
            {"KEY": "here", "EXISTS": None},
            {"KEY": "within", "CONTAINS": "value"},
            {"KEY": "start", "STARTSWITH": "value"},
            {"KEY": "end", "ENDSWITH": "value"},
            {"GOTO": "key", "KEY": "at", "EXISTS": None},
        ],
        [
            "7B000000",
            "220000007400000065000000730000007400000022000000{0-16}64000000610000007400000061000000",
            "2200000066000000690000006C0000006500000022000000{0-16}3A000000{0-16}[30:39]",
            "22000000620000006F0000006F0000006C00000022000000{0-16}3A000000{0-16}(74000000720000007500000065000000|66000000610000006C0000007300000065000000)",
            "220000006800000065000000720000006500000022000000{0-16}3A000000",
            "2200000077000000690000007400000068000000690000006E00000022000000{0-16}3A000000{0-16}22000000*76000000610000006C0000007500000065000000*22000000",
            "22000000730000007400000061000000720000007400000022000000{0-16}3A000000{0-16}2200000076000000610000006C0000007500000065000000",
            "22000000650000006E0000006400000022000000{0-16}3A000000{0-16}*76000000610000006C000000750000006500000022000000",
            "220000006B000000650000007900000022000000{0-16}3A000000",
            "22000000610000007400000022000000{0-16}3A000000",
            "7D000000",
        ],
        "utf-32le",
    ),
    (
        [
            {"INDEX": 1, "KEY": "key", "EXISTS": None},
        ],
        [
            "7B000000",
            "{0-16}5B000000*7B000000*220000006B000000650000007900000022000000{0-16}3A000000*7D000000*5D000000",
            "7D000000",
        ],
        "utf-32le",
    ),
]


@pytest.mark.parametrize("markers, expected, encoding", encoding_tests)
def test_unicode_signatures(markers, expected, encoding):
    """Provide a basic unicode tests.

    These tests are based on the following two sample files:

    ```json
        {
            "test": "data",
            "file": 1,
            "bool": true,
            "here": "random...",
            "within": "_value_",
            "start": "value_",
            "end": "_value",
            "key": {
                "at": "value"
            }
        }
    ```

    ```json
        [
            0,
            {
                "key": "value"
            }
        ]
    ```

    """

    processed = pronom.process_markers(markers, 0, encoding)
    res = []
    for sequence in processed[0].byte_sequences:
        res.append(sequence.value)
    assert res == expected
