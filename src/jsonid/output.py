"""Functions for output of results."""

import json
import logging

try:
    import registry
    import registry_class
    import version
except ModuleNotFoundError:
    try:
        from src.jsonid import registry, registry_class, version
    except ModuleNotFoundError:
        from jsonid import registry, registry_class, version


logger = logging.getLogger(__name__)


def mimeout(results: list):
    """For every result in the result set generate an appropriate
    MIMEType.

    See the associated unit tests for more information on
    expected results.
    """
    res = []
    for item in results:
        # In the first instance, deal with data we have definitively
        # identified using JSONID. Everything else will receive default
        # MIMETypes below.
        if isinstance(item, registry_class.RegistryEntry):
            res.append(
                f'{item.mime[0]}; charset={item.encoding}; doctype="{item.name[0]["@en"]}"; ref={item.identifier}'
            )
            continue
        # Defensive check for the remaining data types we may be
        # working with in this utility. In the fullness of time it
        # should be possible to remove this.
        if not isinstance(item, registry.BaseCharacteristics):
            logger.error("invalid data, cannot output value for: %s", item)
            continue
        # Each remaining `if` works as a precedence. Empty over all.
        # Compression over binary, and so on.
        if item.empty:
            res.append("inode/x-empty; charset=binary")
            continue
        if item.compression:
            res.append(f"{item.compression}; charset=binary")
            continue
        if item.binary:
            res.append("application/octet-stream; charset=binary")
            continue
        if item.text and item.encoding:
            res.append(f"text/plain; charset={item.encoding}")
            continue
        if item.text:
            res.append("text/plain; charset=unknown")
            continue
        res.append("application/octet-stream; charset=unknown")
    return res


def _format_path(path: str):
    """Format the path so that it outputs as neatly as possible.

    NB. also provide an easier way to perform integration testing.
    """
    return f"{path}"


def format_results_for_cli(path: str, padding: int, res: list):
    """Format the results for the CLI.

    Returns a single line per path.
    """
    path_formatted = _format_path(path)
    res_formatted = f'{path_formatted:{padding}}\t[{len(res)}]\t{" | ".join(res)}'
    return res_formatted


def format_results_for_agentout(path: str, res: list):
    """Return a result set that provides more provenance information
    if required, e.g. by a digital preservation system.

    We have elected to output JSON here as it is one of the easier
    formats to map into other formats. It is also easy to work with
    on the command line, e.g. using JQ.
    """
    res = {
        "path": path,
        "results": res,
        "count": len(res),
        "agent": version.get_agent(),
    }
    return json.dumps(res, indent=2)


def output_results(path: str, results: list, padding: int, agentout: bool):
    """Output JSONID results.

    Print is wrapped in print_result to better enable testing, i.e.
    we can assert print_result was called with a given value easier
    and avoid risking false-negatives using standard `print()`.
    """
    res = mimeout(results)
    if agentout:
        res = format_results_for_agentout(path, res)
        print_result(res)
        return
    cli_res = format_results_for_cli(path, padding, res)
    print_result(cli_res)
    return


def print_result(result: str):
    """Wrap print to enable e2e testing."""
    print(result)
