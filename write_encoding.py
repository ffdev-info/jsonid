"""Script to help automatically generate batches of examples of JSON
based on Python encodings.

The examples are added to the samples directory for those curious about
the files themselves. Otherwise these will be tested via the unit
tests through their own self-generating tests.
"""

from pathlib import Path
from typing import Final


def write_json():
    """Write JSON files with different encodings."""

    try:
        encoding_path = Path("samples") / Path("encoding")
        encoding_path.mkdir()
    except FileExistsError:
        pass

    json_map = '{"a": "b"}\n'
    json_list = "[]\n"
    json_int = "123\n"
    json_float = "1.11\n"
    json_map_whitespace = '      \n\n\n\n{"a": "b"}\n'
    json_list_whitespace = "      \n\n\n\n[]\n"
    json_big5 = '{"\u5ee3\u5dde": "\u5ee3\u5dde"}\n'
    json_shift_jis = '{"\u307d\u3063\u3077\u308b\u30e1\u30a4\u30eb": "\u307d\u3063\u3077\u308b\u30e1\u30a4\u30eb"}\n'

    to_write = {
        "map": json_map,
        "list": json_list,
        "int": json_int,
        "float": json_float,
        "map_whitespace": json_map_whitespace,
        "list_whitespace": json_list_whitespace,
        "big5": json_big5,
        "shift_jis": json_shift_jis,
    }

    supported_encodings: Final[list] = [
        "UTF-8",
        "UTF-16",
        "UTF-16LE",
        "UTF-16BE",
        "UTF-32",
        "UTF-32LE",
        "UTF-32BE",
        "BIG5",
        "SHIFT-JIS",
    ]

    for key, value in to_write.items():
        for supported in supported_encodings:
            json_file = encoding_path / f"{supported}-{key}.json"
            json_file.open("w", encoding=supported).write(value)


def main():
    """Primary entry point for this script."""
    write_json()


if __name__ == "__main__":
    main()
