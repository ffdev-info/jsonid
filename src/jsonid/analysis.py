"""Simple module to analys JSON for technical metadata."""

import hashlib
import json
import logging
from typing import Any, Final

import unf
from ipfs_cid import cid_sha256_hash

try:
    import helpers
except ModuleNotFoundError:
    try:
        from src.jsonid import helpers
    except ModuleNotFoundError:
        from jsonid import helpers


logger = logging.getLogger(__name__)

# Provide a sensible default to warn about line length if the object
# occupies a single line only.
LINE_LENGTH: Final[int] = 80


async def unf_fingerprint(data: Any) -> str:
    """Calculate Universal Numerical Fingerprint (UNF) for the data.

    UNF: https://guides.dataverse.org/en/latest/developers/unf/index.html
    """
    res = None
    try:
        res = unf.unf(data)
    except TypeError:
        data_str = json.dumps(data, sort_keys=True)
        res = unf.unf(data_str)
    return res


async def ipld_cid(data: Any):
    """Create a IPLD compatible content identifier.

    Dissect the CID here: https://cid.ipfs.tech/
    """

    d = json.dumps(data, sort_keys=True)
    digest = hashlib.sha256(d.encode()).hexdigest()
    cid_hash = cid_sha256_hash(digest.encode())
    return cid_hash


async def fingerprint(data: Any):
    """fingerprint the json data

    Useful thoughts on normalizing a json-like data structure:

       * https://stackoverflow.com/a/22003440/23789970
    """
    return {
        "unf": await unf_fingerprint(data),
        "cid": await ipld_cid(data),
    }


def analyse_depth(data: Any) -> int:
    """Calculate the depth and potential complexity of the structure.

    Depth is the maximum depth of complex list and dict data-types.
    Empty maps or arrays are not counted, e.g. `[]` and `{}` == 0 where
    `[[]]` and `{"key1":[]} == 1; the latter has a complex type
    containing one item, even if the item is ostensibly `null`.

    Implementation via:

        * https://stackoverflow.com/a/30928645/23789970

    """
    if data and isinstance(data, dict):
        return 1 + max(analyse_depth(data[k]) for k in data)
    if data and isinstance(data, list):
        return 1 + max(analyse_depth(k) for k in data)
    return 0


async def _get_list_types(data: list) -> list:
    """Enumerate the list types, and look for heterogeneous types.

    NB. It should be possible to exit this loop early with a check
    for `len(list) > 0 and type(item) not in list`, but it's not
    working for me as I write.
    """
    types = []
    for item in data:
        types.append(type(item))
        if isinstance(item, list):
            complex_types = await _get_list_types(item)
            if complex_types:
                return True
    if len(set(types)) > 1:
        return True
    return False


async def analyse_list_types(data: Any) -> bool:
    """Return information about the complexity of list objects to
    provide some indivator to developers about when they are
    prociessing lists of odd-complexity, e.g. when processing a list
    of integers, SHOULD you normally have to expect a list type, bool,
    or something  else?

    NB. I have a sense _get_list_types() can be combined with this
    function but maybe at the risk of complexity? (or it simplifies
    things?)

    At time of writing, the current method works quite niccely. Looks
    good, might delete later.
    """
    try:
        values = data.values()
    except AttributeError:
        if not isinstance(data, list):
            return False
        values = data
    complexity = []
    for item in values:
        if isinstance(item, list):
            # Process list, but if list contains a list, we need to
            # recurse.
            complex_types = await _get_list_types(item)
            complexity.append(complex_types)
        if isinstance(item, dict):
            complex_types = await analyse_list_types(item)
            complexity.append(complex_types)
    return True in complexity


async def analyse_all_types(data: Any, all_depths: bool = False):
    """Analyse types at all levels of the object to provide an
    indication of overall complexity, and to provide some idea to
    signature devs about what data to test for. Defaults to just the
    top level to reduce complexity.
    """
    try:
        values = data.values()
    except AttributeError:
        if not isinstance(data, list):
            return [helpers.substitute_type_text(type(data))]
        values = data
    types = []
    for item in values:
        types.append(helpers.substitute_type_text(type(item)))
        if not all_depths:
            continue
        if isinstance(item, list):
            type_ = await analyse_all_types(item, all_depths)
            types.append(type_)
        if isinstance(item, dict):
            type_ = await analyse_all_types(item, all_depths)
            types.append(type_)
    return types


async def analyse_input(data: Any, content: str, all_depths: bool = False):
    """Analyse a given input and output statistics, e.g.

    * No. keys at top level.
    * Key-types at different depths.
    * Identify heterogeneous lists.
    * Depth of complex objects, i.e. nested dicts and lists.

    """
    keys = []
    try:
        keys = data.keys()
    except AttributeError:
        pass
    depth = analyse_depth(data)
    content_length = len(content)
    lines = content.count("\n")
    line_warning = False
    if lines == 1 and len(content) > LINE_LENGTH:
        line_warning = True
    top_level_types = await analyse_all_types(data, all_depths)
    heterogenerous_types = await analyse_list_types(data)
    return {
        "content_length": content_length,
        "number_of_lines": lines,
        "line_warning": line_warning,
        "top_level_keys_count": len(keys),
        "top_level_keys": list(keys),
        "top_level_types": top_level_types,
        "depth": depth,
        "heterogeneous_list_types": heterogenerous_types,
        "fingerprint": await fingerprint(data),
    }
