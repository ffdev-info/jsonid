"""PRONOM export routines.

XML tooling: https://xmllint.com/
"""

import binascii
import codecs
import logging
import xml.dom.minidom
from dataclasses import dataclass
from functools import lru_cache
from typing import Any, Final

try:
    import export_helpers
    import helpers
    import registry_matchers
except ModuleNotFoundError:
    try:
        from src.jsonid import export_helpers, helpers, registry_matchers
    except ModuleNotFoundError:
        from jsonid import export_helpers, helpers, registry_matchers


logger = logging.getLogger(__name__)


DISK_SECTOR_SIZE: Final[int] = 4095

# Common PRONOM characters.
COLON: Final[str] = "3A"
CURLY_OPEN: Final[str] = "7B"
CURLY_CLOSE: Final[str] = "7D"
SQUARE_OPEN: Final[str] = "5B"
SQUARE_CLOSE: Final[str] = "5D"
DOUBLE_QUOTE: Final[str] = "22"

# Constant values.
NUMBER_REGEX: Final[str] = "[30:39]"
TRUE_VALUE: Final[str] = "74727565"
FALSE_VALUE: Final[str] = "66616C7365"
NULL_VALUE: Final[str] = "6E756C6C"

# Our whitespace values could potentially be optimized per encoding,
# e.g. to be more or less per encoding. 16 is a good default to enable
# some UTF32-identification.
WHITESPACE_REGEX: Final[str] = "{0-16}"

# External signature types.
EXT: Final[str] = "file extension"

# Replacement markers for PRONOM pre-processing.
MARKER_INDEX_START = "INDEX_START"
MARKER_INDEX_END = "INDEX END"


class UnprocessableEntity(Exception):
    """Provide a way to give complete feedback to the caller to allow
    it to exit."""


@dataclass
class ExternalSignature:
    id: str
    signature: str
    type: str


@dataclass
class ByteSequence:
    id: str
    pos: str
    min_off: str
    max_off: str
    endian: str
    value: str


@dataclass
class InternalSignature:
    id: str
    name: str
    byte_sequences: list[ByteSequence]


@dataclass
class Priority:
    type: str
    id: str


@dataclass
class Identifier:
    type: str
    value: str


@dataclass
class Format:  # pylint: disable=R0902
    id: str
    name: str
    version: str
    puid: str
    mime: str
    classification: str
    external_signatures: list[ExternalSignature]
    internal_signatures: list[InternalSignature]
    priorities: list[int]


@lru_cache()
def _get_bom() -> list:
    """Generate a list of byte-order markers that allow us to replace
    markers introduced through various encoding operations.
    """
    replaces = [
        codecs.BOM,
        codecs.BOM_BE,
        codecs.BOM_LE,
        codecs.BOM_UTF8,
        codecs.BOM_UTF16,
        codecs.BOM_UTF16_BE,
        codecs.BOM_UTF16_LE,
        codecs.BOM_UTF32,
        codecs.BOM_UTF32_BE,
        codecs.BOM_UTF32_LE,
    ]
    res = []
    for bom in replaces:
        hex_bom = ""
        for marker in bom:
            char = hex(marker)
            hex_bom = f"{hex_bom}{char.replace('0x', '')}".upper()
        res.append(hex_bom)
    return res


def create_many_to_one_byte_sequence(internal_signatures: list[InternalSignature]):
    """Create a many to one byte sequence, i.e. a format with multiple
    Internal Signatures.
    """
    internal_signature = ""
    for internal in internal_signatures:
        id_ = internal.id
        bs = create_one_to_many_byte_sequence(internal.byte_sequences)
        internal_signature = f"""
{internal_signature}<InternalSignature ID=\"{id_}\" Specificity=\"Specific\">
    {bs}
</InternalSignature>
        """
    return internal_signature.strip()


def calculate_variable_off_bof(item: ByteSequence):
    """Given variable offsets, calculate the correct syntax."""
    seq = item.value
    if (
        item.min_off != ""
        and int(item.min_off) > 0
        and item.max_off != ""
        and int(item.max_off) > 0
    ):
        seq = f"{{{item.min_off}-{int(item.min_off)+int(item.max_off)}}}{seq}"
    elif item.max_off != "" and int(item.max_off) > 0:
        seq = f"{{0-{item.max_off}}}{seq}"
    elif item.min_off != "" and int(item.min_off) > 0:
        seq = f"{{{item.min_off}}}{seq}"
    return seq


def calculate_variable_off_eof(item: ByteSequence):
    """Given variable offsets, calculate the correct syntax."""
    seq = item.value
    if (
        item.min_off != ""
        and int(item.min_off) > 0
        and item.max_off != ""
        and int(item.max_off) > 0
    ):
        seq = f"{seq}{{{item.min_off}-{int(item.min_off)+int(item.max_off)}}}"
    elif item.max_off != "" and int(item.max_off) > 0:
        seq = f"{seq}{{0-{item.max_off}}}"
    elif item.min_off != "" and int(item.min_off) > 0:
        seq = f"{seq}{{{item.min_off}}}"
    return seq


def create_one_to_many_byte_sequence(byte_sequences: list[ByteSequence]):
    """Create a byte sequence object."""
    byte_sequence = ""
    for item in byte_sequences:
        seq = item.value
        if item.pos.startswith("EOF"):
            seq = calculate_variable_off_eof(item)
        elif item.pos.startswith("BOF"):
            seq = calculate_variable_off_bof(item)
        byte_sequence = f"""
{byte_sequence.strip()}
    <ByteSequence Reference=\"{item.pos}\" Sequence=\"{seq}\" MinOffset=\"{item.min_off}\" MaxOffset=\"{item.max_off}\"/>
        """
    return byte_sequence.strip()


def create_file_format_collection(fmt: list[Format]):
    """Create the FileFormatCollection object.

    E.g.
    ```
        <FileFormat ID="1" Name="Development Signature" PUID="dev/1" Version="1.0" MIMEType="application/octet-stream">
            <InternalSignatureID>1</InternalSignatureID>
            <Extension>ext</Extension>
        </FileFormat>

        <FileFormat ID="49" MIMEType="application/postscript"  FormatType="Text (Structured)"
            Name="Adobe Illustrator" PUID="x-fmt/20" Version="1.0 / 1.1">
            <InternalSignatureID>880</InternalSignatureID>
            <InternalSignatureID>881</InternalSignatureID>
            <Extension>ai</Extension>
            <HasPriorityOverFileFormatID>86</HasPriorityOverFileFormatID>
            <HasPriorityOverFileFormatID>331</HasPriorityOverFileFormatID>
            <HasPriorityOverFileFormatID>332</HasPriorityOverFileFormatID>
            <HasPriorityOverFileFormatID>771</HasPriorityOverFileFormatID>
            <HasPriorityOverFileFormatID>773</HasPriorityOverFileFormatID>
        </FileFormat>
    ```

    """
    internal_sigs = [
        f"<InternalSignatureID>{sig.id}</InternalSignatureID>"
        for sig in fmt.internal_signatures
    ]
    external_sigs = [
        f"<Extension>{sig.signature}</Extension>"
        for sig in fmt.external_signatures
        if sig.type.lower() == EXT
    ]
    priorities = [
        f"<HasPriorityOverFileFormatID>{priority}</HasPriorityOverFileFormatID>"
        for priority in fmt.priorities
    ]
    ff = f"""
<FileFormat ID=\"{fmt.id}\" Name=\"{fmt.name}\" PUID=\"{fmt.puid}\" Version="{fmt.version}" MIMEType=\"{fmt.mime}\" FormatType=\"{fmt.classification}\" >
    {"".join(internal_sigs).strip()}
    {"".join(external_sigs).strip()}
    {"".join(priorities).strip()}
</FileFormat>
    """
    return ff.strip()


def _process_formats(formats: list[Format]):
    """Process formats into a PRONOM XML file."""
    isc = []
    ffc = []
    for fmt in formats:
        ffc.append(create_file_format_collection(fmt))
        if fmt.internal_signatures:
            isc.append(create_many_to_one_byte_sequence(fmt.internal_signatures))
    droid_template = f"""
<?xml version="1.0" encoding="UTF-8"?>
<FFSignatureFile xmlns='http://www.nationalarchives.gov.uk/pronom/SignatureFile' Version='1' DateCreated='{export_helpers.get_utc_timestamp_now()}'>
    <InternalSignatureCollection>
        {"".join(isc).strip()}
    </InternalSignatureCollection>
    <FileFormatCollection>
        {"".join(ffc).strip()}
    </FileFormatCollection>
</FFSignatureFile>
    """
    dom = None
    signature_file = droid_template.strip().replace("\n", "")
    try:
        dom = xml.dom.minidom.parseString(signature_file)
    except xml.parsers.expat.ExpatError as err:
        logger.error("cannot process xml: %s", err)
        return ""
    pretty_xml = dom.toprettyxml(indent=" ", encoding="utf-8")
    prettier_xml = export_helpers.new_prettify(pretty_xml)
    return prettier_xml


def process_formats_and_save(formats: list[Format], filename: str):
    """Process the collected formats and output a signature file.

    NB. Given our dataclasses here, we have the opportunity to rework
    this data into many new structures. We output XML because DROID
    expects XML.
    """
    prettier_xml = _process_formats(formats)
    logger.info("outputting to: %s", filename)
    with open(filename, "w", encoding="utf=8") as output_file:
        output_file.write(prettier_xml)


def process_formats_to_stdout(formats: list[Format]):
    """Process the collected formats and output a signature file.

    NB. Given our dataclasses here, we have the opportunity to rework
    this data into many new structures. We output XML because DROID
    expects XML.
    """
    prettier_xml = _process_formats(formats)
    logger.info("outputting to: stdout")
    print(prettier_xml)


def encode_roundtrip(hexed_val: str, encoding: str) -> str:
    """We want to get a plain-text byte-sequence into a new
    encoding. It takes a few hops and skips.
    """
    val = hexed_val.strip()
    try:
        re_encoded = binascii.unhexlify(hexed_val).decode("utf-8").encode(encoding)
    except (binascii.Error, UnicodeDecodeError) as err:
        logger.error("cannot convert: %s len: %s ('%s')", hexed_val, len(val), err)
        return val
    hex_val = binascii.hexlify(re_encoded).decode().upper()
    for bom in _get_bom():
        if not hex_val.startswith(bom):
            continue
        return hex_val.replace(bom, "")
    return hex_val


def _type_to_str(type_: type, encoding: str) -> str:
    """Given a data type marker we need to convert the type into a
    byte sequence that will match the type.

    E.g. BOOLEAN types evaluate to true or false encoded in ASCII.
    E.g. STRING types need to begin and end with double-quotes but the
         string itself is just a wildcard. The wildcard will match any
         value between the double quotes.
    """

    curly_open_encoded = encode_roundtrip(CURLY_OPEN, encoding)
    curly_close_encoded: Final[str] = encode_roundtrip(CURLY_CLOSE, encoding)
    square_open_encoded: Final[str] = encode_roundtrip(SQUARE_OPEN, encoding)
    square_close_encoded: Final[str] = encode_roundtrip(SQUARE_CLOSE, encoding)
    double_quote_encoded: Final[str] = encode_roundtrip(DOUBLE_QUOTE, encoding)

    try:
        type_ = helpers.substitute_type_text(type_)
    except AttributeError:
        logger.debug("type_ already converted: %s", type_)

    if type_ in (helpers.TYPE_INTEGER, type_ == helpers.TYPE_FLOAT):
        # an integer field will begin 0-9 but it is unclear how to
        # represent larger numbers? and whether we need to?
        return NUMBER_REGEX
    if type_ == helpers.TYPE_BOOL:
        # true | false
        return f"({encode_roundtrip(TRUE_VALUE, encoding)}|{encode_roundtrip(FALSE_VALUE, encoding)})"
    if type_ == helpers.TYPE_STRING:
        # string begins with a double quote and ends in a double quote.
        return f"'{double_quote_encoded}*{double_quote_encoded}"
    if type_ == helpers.TYPE_MAP:
        # { == 7B; } == 7D
        return f"{curly_open_encoded}*{curly_close_encoded}"
    if type_ == helpers.TYPE_LIST:
        # [ == 5B; ] == 5D
        return f"{square_open_encoded}*{square_close_encoded}"
    if type_ == helpers.TYPE_NONE:
        # null
        return f"{encode_roundtrip(NULL_VALUE, encoding)}".encode(encoding)
    # This should only trigger for incorrect values at this point..
    raise UnprocessableEntity(f"type_to_str: {type_}")


def _complex_is_type(marker: Any) -> str:
    """Complex IS might be another data structure, e.g. a dict, or
    something else that we can't convert easily. It is simply a WIP
    for now.
    """
    raise UnprocessableEntity(f"complex IS type: '{marker}' (WIP)")


def _str_to_hex_str(string: str) -> str:
    """Convert string to hexadecimal bytes.

    We convert to bytes here first without encoding and then convert
    the bytes to an encoding second. It should be possible to combine
    those two procedures, but this has worked well during the
    prototyping phase.
    """
    hex_bytes = []
    for byte_ in string.encode():
        hex_bytes.append(hex(byte_).replace("0x", ""))
    hex_str = "".join(hex_bytes).upper()
    return hex_str


def quote_and_encode(value, encoding) -> str:
    """Quote and encode a given value."""

    double_quote_encoded: Final[str] = encode_roundtrip(DOUBLE_QUOTE, encoding)
    # return f"{double_quote_encoded}{value}{double_quote_encoded}"
    return f"{double_quote_encoded}{encode_roundtrip(value, encoding)}{double_quote_encoded}"


def convert_marker_to_signature_sequence(marker: dict, encoding: str) -> str:
    """Convert a JSONID marker into a signature sequence."""

    # pylint: disable=R0914; too-many local variables.
    # pylint: disable=R0911; too-many return statements.
    # pylint: disable=R0915; too-many statements.

    logger.debug("marker: %s", marker)

    colon_encoded: Final[str] = encode_roundtrip(COLON, encoding)
    double_quote_encoded: Final[str] = encode_roundtrip(DOUBLE_QUOTE, encoding)
    curly_open_encoded: Final[str] = encode_roundtrip(CURLY_OPEN, encoding)
    curly_close_encoded: Final[str] = encode_roundtrip(CURLY_CLOSE, encoding)
    colon_encoded: Final[str] = encode_roundtrip(COLON, encoding)
    square_open_encoded: Final[str] = encode_roundtrip(SQUARE_OPEN, encoding)
    square_close_encoded: Final[str] = encode_roundtrip(SQUARE_CLOSE, encoding)
    double_quote_encoded: Final[str] = encode_roundtrip(DOUBLE_QUOTE, encoding)

    instruction = ""
    if registry_matchers.MARKER_GOTO in marker.keys():
        # GOTO KEY and match KEY.
        goto_key = _str_to_hex_str(marker["GOTO"])
        key_at_goto = _str_to_hex_str(marker["KEY"])
        goto_encoded = quote_and_encode(goto_key, encoding)
        key_encoded = quote_and_encode(key_at_goto, encoding)
        instruction = f"{goto_encoded}{WHITESPACE_REGEX}{colon_encoded}*{WHITESPACE_REGEX}{key_encoded}{WHITESPACE_REGEX}{colon_encoded}"
        marker.pop("GOTO")
        marker.pop("KEY")
        return instruction.upper()
    if registry_matchers.MARKER_INDEX in marker.keys():
        key = _str_to_hex_str(marker["KEY"])
        instruction = f"{WHITESPACE_REGEX}{square_open_encoded}*{curly_open_encoded}*{double_quote_encoded}{encode_roundtrip(key, encoding)}{double_quote_encoded}{WHITESPACE_REGEX}{colon_encoded}*{curly_close_encoded}*{square_close_encoded}"
        marker.pop("INDEX")
        marker.pop("KEY")
        return instruction.upper()
    if "KEY" in marker.keys():
        key = _str_to_hex_str(marker["KEY"])
        instruction = quote_and_encode(key, encoding)
        marker.pop("KEY")
    if registry_matchers.MARKER_KEY_EXISTS in marker.keys():
        instruction = f"{instruction}{WHITESPACE_REGEX}{colon_encoded}".upper()
        return instruction
    if registry_matchers.MARKER_IS_TYPE in marker.keys():
        is_type = _type_to_str(marker["ISTYPE"], encoding=encoding)
        type_val = (
            f"{instruction}{WHITESPACE_REGEX}{colon_encoded}{WHITESPACE_REGEX}{is_type}"
        )
        return type_val.upper()
    if registry_matchers.MARKER_IS in marker.keys():
        marker_is = marker["IS"]
        if not isinstance(marker_is, str):
            _complex_is_type(marker_is)
        equals = _str_to_hex_str(marker_is)
        is_val = f"{instruction}{WHITESPACE_REGEX}{encode_roundtrip(equals, encoding)}"
        return is_val.upper()
    if registry_matchers.MARKER_STARTSWITH in marker.keys():
        starts_with = _str_to_hex_str(marker["STARTSWITH"])
        starts_with_val = f"{instruction}{WHITESPACE_REGEX}{colon_encoded}{WHITESPACE_REGEX}{double_quote_encoded}{encode_roundtrip(starts_with, encoding)}"
        return starts_with_val.upper()
    if registry_matchers.MARKER_ENDSWITH in marker.keys():
        ends_with = _str_to_hex_str(marker["ENDSWITH"])
        ends_with_val = f"{instruction}{WHITESPACE_REGEX}{colon_encoded}{WHITESPACE_REGEX}*{encode_roundtrip(ends_with, encoding)}{double_quote_encoded}"
        return ends_with_val.upper()
    if registry_matchers.MARKER_CONTAINS in marker.keys():
        contains = _str_to_hex_str(marker["CONTAINS"])
        contains_val = f"{instruction}{WHITESPACE_REGEX}{colon_encoded}{WHITESPACE_REGEX}{double_quote_encoded}*{encode_roundtrip(contains, encoding)}*{double_quote_encoded}"
        return contains_val.upper()
    if registry_matchers.MARKER_REGEX in marker.keys():
        raise UnprocessableEntity("REGEX not yet implemented")
    if registry_matchers.MARKER_KEY_NO_EXIST in marker.keys():
        raise UnprocessableEntity("KEY NO EXIST not yet implemented")
    # We should never arrive here. In the future clean this up so we
    # only return when we have information.
    return ""


def preprocess_goto_markers(markers: dict) -> list:
    """Preprocess markers to remove data that is otherwise duplicated
    when converted to a PRONOM signature, e.g. GOTO."""

    out = []
    for marker in markers:
        if registry_matchers.MARKER_GOTO not in marker:
            out.append(marker)
            continue
        key = marker.pop("GOTO")
        new_marker = {"KEY": key, "EXISTS": None}
        if new_marker not in out:
            out.append(new_marker)
        out.append(marker)
    return out


def process_markers(
    markers: list, sig_id: int, encoding: str = ""
) -> tuple[list | bool]:
    """Given a set of markers for a document type, process them into
    a set of byte sequences and finally an internal signature sequence
    that can be output as a PRONOM signature.

    returns a tuple describing the processed value and a flag to
    highlight the result is potentially lossless, e.g. in the case
    of matching types, e.g. strings.

    dict_keys(['CONTAINS'])
    dict_keys(['ENDSWITH'])
    dict_keys(['IS']
    dict_keys(['ISTYPE'])
    dict_keys(['STARTSWITH'])

    key(0-n):(0-n)value

    Need to return something like:

      <ByteSequence Reference="BOFoffset" Sequence="FFD8FFE0{2}4A464946000101(00|01|02)" MinOffset="0" MaxOffset=""/>

    Different encodings need to be accounted for, e.g. (with added
    whitespace below)

    UTF-32-LE:

        00000000: 2000 0000 2000 0000 2000 0000 2000 0000   ... ... ... ...
        00000010: 2000 0000 2000 0000 0a00 0000 0a00 0000   ... ...........
        00000020: 0a00 0000 0a00 0000 7b00 0000 2200 0000  ........{..."...
        00000030: 6100 0000 2200 0000 3a00 0000 2000 0000  a..."...:... ...
        00000040: 2200 0000 6200 0000 2200 0000 7d00 0000  "...b..."...}...
        00000050: 0a00 0000                                ....

    UTF-32-BE:

        00000000: 0000 0020 0000 0020 0000 0020 0000 0020  ... ... ... ...
        00000010: 0000 0020 0000 0020 0000 000a 0000 000a  ... ... ........
        00000020: 0000 000a 0000 000a 0000 007b 0000 0022  ...........{..."
        00000030: 0000 0061 0000 0022 0000 003a 0000 0020  ...a..."...:...
        00000040: 0000 0022 0000 0062 0000 0022 0000 007d  ..."...b..."...}
        00000050: 0000 000a                                ....


    UTF-16-LE:

        00000000: 2000 2000 2000 2000 2000 2000 0a00 0a00   . . . . . .....
        00000010: 0a00 0a00 7b00 2200 6100 2200 3a00 2000  ....{.".a.".:. .
        00000020: 2200 6200 2200 7d00 0a00                 ".b.".}...

    UTF-16-BE:

        00000000: 0020 0020 0020 0020 0020 0020 000a 000a  . . . . . . ....
        00000010: 000a 000a 007b 0022 0061 0022 003a 0020  .....{.".a.".:.
        00000020: 0022 0062 0022 007d 000a                 .".b.".}..


    """

    curly_open_encoded: Final[str] = encode_roundtrip(CURLY_OPEN, encoding)
    curly_close_encoded: Final[str] = encode_roundtrip(CURLY_CLOSE, encoding)

    sequences = []

    markers = preprocess_goto_markers(markers)

    for marker in markers:
        sig_sequence = convert_marker_to_signature_sequence(marker, encoding)
        sequences.append(sig_sequence)

    byte_sequences = []

    byte_sequences.append(
        ByteSequence(
            id=0,
            pos="BOF",
            min_off=0,
            max_off=f"{DISK_SECTOR_SIZE}",
            endian="",
            value=curly_open_encoded,
        )
    )

    for idx, item in enumerate(sequences, 0):
        logger.debug("%s. %s", idx, item)
        byte_sequence = ByteSequence(
            id=idx,
            pos="VAR",
            min_off="",
            max_off="",
            endian="",
            value=item,
        )
        byte_sequences.append(byte_sequence)

    byte_sequences.append(
        ByteSequence(
            id=0,
            pos="EOF",
            min_off="0",
            max_off=f"{DISK_SECTOR_SIZE}",
            endian="",
            value=curly_close_encoded,
        )
    )

    internal_signature = InternalSignature(
        id=sig_id,
        name="",
        byte_sequences=byte_sequences,
    )

    return [internal_signature]


def create_baseline_json_sequences(encoding: str):
    """Create baseline JSON sequences that match map and list types
    with various different encodings.
    """

    # pylint: disable=R0914; too-many local variables.

    curly_open_encoded: Final[str] = encode_roundtrip(CURLY_OPEN, encoding)
    curly_close_encoded: Final[str] = encode_roundtrip(CURLY_CLOSE, encoding)
    square_open_encoded: Final[str] = encode_roundtrip(SQUARE_OPEN, encoding)
    square_close_encoded: Final[str] = encode_roundtrip(SQUARE_CLOSE, encoding)

    colon_encoded: Final[str] = encode_roundtrip(COLON, encoding)
    double_quote_encoded: Final[str] = encode_roundtrip(DOUBLE_QUOTE, encoding)

    bof = f"({curly_open_encoded}|{square_open_encoded})"
    eof = f"({curly_close_encoded}|{square_close_encoded})"

    no_encoded: Final[str] = NUMBER_REGEX
    true_encoded: Final[str] = encode_roundtrip(TRUE_VALUE, encoding)
    false_encoded: Final[str] = encode_roundtrip(FALSE_VALUE, encoding)
    null_encoded: Final[str] = encode_roundtrip(NULL_VALUE, encoding)

    options = (
        f"{double_quote_encoded}{WHITESPACE_REGEX}{colon_encoded}",
        no_encoded,
        f"({true_encoded}|{false_encoded})",
        null_encoded,
    )

    sigs = []

    for opt in options:

        bs = []

        bs.append(
            ByteSequence(
                id=1,
                pos="BOF",
                min_off=0,
                max_off=f"{DISK_SECTOR_SIZE}",
                endian="",
                value=bof,
            )
        )

        bs.append(
            ByteSequence(
                id=1,
                pos="VAR",
                min_off=0,
                max_off=0,
                endian="",
                value=opt,
            )
        )

        bs.append(
            ByteSequence(
                id=1,
                pos="EOF",
                min_off="0",
                max_off=f"{DISK_SECTOR_SIZE}",
                endian="",
                value=eof,
            )
        )

        iss = InternalSignature(
            id=0,
            name="",
            byte_sequences=bs,
        )

        sigs.append(iss)

    return sigs
