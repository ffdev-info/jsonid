"""JSON registry processor. """

import copy
import json
import logging
from dataclasses import dataclass
from typing import Any, Final, Union

try:
    import analysis
    import registry_class
    import registry_data
    import registry_matchers
except ModuleNotFoundError:
    try:
        from src.jsonid import (
            analysis,
            registry_class,
            registry_data,
            registry_matchers,
        )
    except ModuleNotFoundError:
        from jsonid import analysis, registry_class, registry_data, registry_matchers


logger = logging.getLogger(__name__)


class IdentificationFailure(Exception):
    """Raise when identification fails."""


DOCTYPE_JSON: Final[str] = "JSON"
DOCTYPE_JSONL: Final[str] = "JSONL"
DOCTYPE_YAML: Final[str] = "YAML"
DOCTYPE_TOML: Final[str] = "TOML"

NIL_ENTRY: Final[registry_class.RegistryEntry] = registry_class.RegistryEntry()

IS_JSON: Final[str] = "parses as JSON but might not conform to a schema"
IS_JSONL: Final[str] = "parses as JSONL but might not conform to a schema"
IS_YAML: Final[str] = "parses as YAML but might not conform to a schema"
IS_TOML: Final[str] = "parses as TOML but might not conform to a schema"

TYPE_LIST: Final[list] = [{"@en": "data is list type"}]
TYPE_DICT: Final[list] = [{"@en": "data is map (dict) type"}]
TYPE_NONE: Final[list] = [{"@en": "data is null"}]
TYPE_FLOAT: Final[list] = [{"@en": "data is float type"}]
TYPE_INT: Final[list] = [{"@en": "data is integer type"}]
TYPE_BOOL: Final[list] = [{"@en": "data is boolean type"}]
TYPE_ERR: Final[list] = [{"@en": "error processing data"}]

JSON_ONLY: Final[registry_class.RegistryEntry] = registry_class.RegistryEntry(
    identifier=registry_class.JSON_ID,
    name=[{"@en": "JavaScript Object Notation (JSON)"}],
    description=[{"@en": IS_JSON}],
    version=None,
    rfc="https://datatracker.ietf.org/doc/html/rfc8259",
    pronom="http://www.nationalarchives.gov.uk/PRONOM/fmt/817",
    loc="https://www.loc.gov/preservation/digital/formats/fdd/fdd000381.shtml",
    wikidata="https://www.wikidata.org/entity/Q2063",
    archive_team="http://fileformats.archiveteam.org/wiki/JSON",
    mime=["application/json"],
    markers=None,
)

JSONL_ONLY: Final[registry_class.RegistryEntry] = registry_class.RegistryEntry(
    identifier=registry_class.JSONL_ID,
    name=[{"@en": "JSONLines (JSONL)"}],
    description=[{"@en": IS_JSONL}],
    version=None,
    rfc="",
    pronom="http://www.nationalarchives.gov.uk/PRONOM/fmt/2054",
    loc="",
    wikidata="https://www.wikidata.org/entity/Q111841144",
    archive_team="",
    mime=["application/jsonl"],
    markers=None,
)

YAML_ONLY: Final[registry_class.RegistryEntry] = registry_class.RegistryEntry(
    identifier=registry_class.YAML_ID,
    name=[{"@en": "YAML (YAML another markup language / YAML ain't markup language)"}],
    description=[{"@en": IS_YAML}],
    version=None,
    pronom="http://www.nationalarchives.gov.uk/PRONOM/fmt/818",
    wikidata="https://www.wikidata.org/entity/Q281876",
    archive_team="http://fileformats.archiveteam.org/wiki/YAML",
    loc="https://www.loc.gov/preservation/digital/formats/fdd/fdd000645.shtml",
    mime=["application/yaml"],
    markers=None,
)

TOML_ONLY: Final[registry_class.RegistryEntry] = registry_class.RegistryEntry(
    identifier=registry_class.TOML_ID,
    name=[{"@en": "Tom's Obvious, Minimal Language (TOML)"}],
    description=[{"@en": IS_TOML}],
    version=None,
    wikidata="https://www.wikidata.org/entity/Q28449455",
    archive_team="http://fileformats.archiveteam.org/wiki/TOML",
    mime=["application/toml"],
    markers=None,
)

REGISTERED: Final[str] = (DOCTYPE_JSON, DOCTYPE_JSONL, DOCTYPE_YAML, DOCTYPE_TOML)
CORE_RECORDS: Final[str] = [JSON_ONLY, JSONL_ONLY, YAML_ONLY, TOML_ONLY]


@dataclass
class BaseCharacteristics:
    """BaseCharacteristics wraps information about the base object
    for ease of moving it through the code to where we need it.

    NB. one consideration is what to do with the term `valid` here. It
    is doing more work than necessary. It is both, not valid text, and
    not valid object type, i.e. JSON,YAML,TOML etc. It's probably
    too broad and might cause inconsistent results. We should observe
    `binary` output and make sure it works as expected.
    """

    # Too many instance attributes.
    # pylint: disable=R0902

    # valid describes whether or not the object has been parsed
    # correctly.
    valid: bool = False
    # data represents the Data as parsed by the utility.
    data: Union[Any, None] = None
    # doctype describes the object type we have identified.
    doctype: Union[str, None] = None
    # encoding describes the character encoding of the object.
    encoding: Union[str, None] = None
    # content_for_analysis is the string/byte data that was the
    # original object and is used in the structural analysis of
    # the object.
    content_for_analysis: Union[str, None] = None
    # compression describes whether or not the object was originally
    # compressed before identification. (JSONL only)
    compression: Union[str, None] = None
    # content is binary content.
    binary: bool = False
    # content is text. NB. This may be redundant in the fullness of
    # time, but to begin with we will try to be as explicit as
    # possible to ensure the accuracy of the output.
    text: bool = False
    # file is empty.
    empty: bool = False
    # file only contains whitespace.
    only_whitespace: bool = False


def _get_language(string_field: list[dict], language: str = "@en") -> str:
    """Return a string in a given language from a result string."""
    for value in string_field:
        try:
            return value[language]
        except KeyError:
            pass
    return string_field[0]


def _get_core(doctype: str) -> registry_class.RegistryEntry:
    """Return a version of a core registry object when requested."""
    if doctype == DOCTYPE_JSON:
        return copy.deepcopy(JSON_ONLY)
    if doctype == DOCTYPE_JSONL:
        return copy.deepcopy(JSONL_ONLY)
    if doctype == DOCTYPE_YAML:
        return copy.deepcopy(YAML_ONLY)
    if doctype == DOCTYPE_TOML:
        return copy.deepcopy(TOML_ONLY)
    return copy.deepcopy(NIL_ENTRY)


def get_additional(data: Union[dict, list, float, int]) -> str:
    """Return additional characterization information about the JSON
    we encountered.
    """

    # pylint: disable=R0911

    if not data:
        if data is False:
            return TYPE_BOOL
        if isinstance(data, list):
            return TYPE_LIST
        if isinstance(data, dict):
            return TYPE_DICT
        return TYPE_NONE
    if isinstance(data, dict):
        return TYPE_DICT
    if isinstance(data, list):
        return TYPE_LIST
    if isinstance(data, float):
        return TYPE_FLOAT
    if isinstance(data, int):
        if data is True:
            return TYPE_BOOL
        return TYPE_INT
    return TYPE_ERR


def process_markers(registry_entry: registry_class.RegistryEntry, data: dict) -> bool:
    """Run through the markers for an entry in the registry.
    Attempt to exit early if there isn't a match.
    """

    # pylint: disable=R0911,R0912.R0915

    if isinstance(data, list):
        for marker in registry_entry.markers:
            try:
                _ = marker[registry_matchers.MARKER_INDEX]
                data = registry_matchers.at_index(marker, data)
                break
            except KeyError:
                return False
    top_level_pointer = data  # ensure we're always looking at top-level dict
    for marker in registry_entry.markers:
        data = top_level_pointer
        try:
            _ = marker[registry_matchers.MARKER_GOTO]
            data = registry_matchers.at_goto(marker, data)
        except KeyError as err:
            logger.debug("following through: %s", err)
        try:
            _ = marker[registry_matchers.MARKER_CONTAINS]
            match = registry_matchers.contains_match(marker, data)
            if not match:
                return False
        except KeyError as err:
            logger.debug("following through: %s", err)
        try:
            _ = marker[registry_matchers.MARKER_STARTSWITH]
            match = registry_matchers.startswith_match(marker, data)
            if not match:
                return False
        except KeyError as err:
            logger.debug("following through: %s", err)
        try:
            _ = marker[registry_matchers.MARKER_ENDSWITH]
            match = registry_matchers.endswith_match(marker, data)
            if not match:
                return False
        except KeyError as err:
            logger.debug("following through: %s", err)
        try:
            _ = marker[registry_matchers.MARKER_IS]
            match = registry_matchers.is_match(marker, data)
            if not match:
                return False
        except KeyError as err:
            logger.debug("following through: %s", err)
        try:
            _ = marker[registry_matchers.MARKER_IS_TYPE]
            match = registry_matchers.is_type(marker, data)
            if not match:
                return False
        except KeyError as err:
            logger.debug("following through: %s", err)
        try:
            _ = marker[registry_matchers.MARKER_REGEX]
            match = registry_matchers.regex_match(marker, data)
            if not match:
                return False
        except KeyError as err:
            logger.debug("following through: %s", err)
        try:
            _ = marker[registry_matchers.MARKER_KEY_EXISTS]
            match = registry_matchers.key_exists_match(marker, data)
            if not match:
                return False
        except KeyError as err:
            logger.debug("following through: %s", err)
        try:
            _ = marker[registry_matchers.MARKER_KEY_NO_EXIST]
            match = registry_matchers.key_no_exist_match(marker, data)
            if not match:
                return False
        except KeyError as err:
            logger.debug("following through: %s", err)
    return True


def build_identifier(
    registry_entry: registry_class.RegistryEntry,
    base_obj: BaseCharacteristics,
) -> registry_class.RegistryEntry:
    """Create a match object to return to the caller. For the
    identifier and borrowing from MIMETypes buuld a hierarchical
    identifier using the registry identifier and the doctype,
    e.g. yaml, json, etc.
    """
    match_obj = copy.deepcopy(registry_entry)
    match_obj.encoding = base_obj.encoding
    core = _get_core(base_obj.doctype)
    match_obj.mime = core.mime
    if base_obj.compression:
        match_obj.mime = base_obj.compression
    if base_obj.doctype == DOCTYPE_JSONL:
        try:
            suffix = base_obj.compression.split("/")[1]
            match_obj.mime = [f"{mime}+{suffix}" for mime in core.mime]
        except AttributeError:
            pass
    return match_obj


def matcher(base_obj: BaseCharacteristics) -> list:
    """Matcher for registry objects."""
    logger.debug("type: '%s'", type(base_obj.data))
    if isinstance(base_obj.data, str):
        try:
            base_obj.data = json.loads(base_obj.data)
        except json.decoder.JSONDecodeError as err:
            logger.error("unprocessable data: %s", err)
            return []
    reg = registry_data.registry()
    matches = []
    for idx, registry_entry in enumerate(reg):
        try:
            logger.debug("processing registry entry: %s", idx)
            match = process_markers(registry_entry, base_obj.data)
            if not match:
                continue
            if registry_entry in matches:
                continue
            match_obj = build_identifier(registry_entry, base_obj)
            matches.append(match_obj)
        except TypeError as err:
            logger.debug("%s", err)
            continue
    if len(matches) == 0 or matches[0] == NIL_ENTRY:
        additional = get_additional(base_obj.data)
        res_obj = registry_class.RegistryEntry()
        if base_obj.doctype == DOCTYPE_JSON:
            res_obj = JSON_ONLY
            res_obj.depth = analysis.analyse_depth(base_obj.data)
        elif base_obj.doctype == DOCTYPE_JSONL:
            # NB. JSONL does not have a depth calculation we can
            # use at this point in the analysis. This can only be
            # output via the analysis switch.
            res_obj = JSONL_ONLY
        elif base_obj.doctype == DOCTYPE_YAML:
            res_obj = YAML_ONLY
            res_obj.depth = analysis.analyse_depth(base_obj.data)
        elif base_obj.doctype == DOCTYPE_TOML:
            res_obj = TOML_ONLY
            res_obj.depth = analysis.analyse_depth(base_obj.data)
        res_obj.additional = additional
        res_obj.encoding = base_obj.encoding
        res_obj = build_identifier(res_obj, base_obj)
        return [res_obj]
    logger.debug(matches)
    return matches
