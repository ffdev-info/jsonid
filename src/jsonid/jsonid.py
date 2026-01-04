"""jsonid entry-point."""

# pylint: disable=C0103,W0603

import argparse
import asyncio
import logging
import signal
import sys
import time
from typing import Final

try:
    import export
    import file_processing
    import helpers
    import lookup
    import registry
except ModuleNotFoundError:
    try:
        from src.jsonid import export, file_processing, helpers, lookup, registry
    except ModuleNotFoundError:
        from jsonid import export, file_processing, helpers, lookup, registry


logger = None


decode_strategies: Final[list] = [
    registry.DOCTYPE_JSON,
    registry.DOCTYPE_JSONL,
    registry.DOCTYPE_YAML,
    registry.DOCTYPE_TOML,
]


def init_logging(debug: bool):
    """Initialize logging."""
    logging.basicConfig(
        format="%(asctime)-15s %(levelname)s :: %(filename)s:%(lineno)s:%(funcName)s() :: %(message)s",  # noqa: E501
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.DEBUG if debug else logging.INFO,
        handlers=[
            logging.StreamHandler(),
        ],
    )
    logging.Formatter.converter = time.gmtime
    global logger
    logger = logging.getLogger(__name__)
    logger.debug("debug logging is configured")


def _attempt_lookup(args: argparse.Namespace):
    """Attempt to lookup a registry entry in the database."""
    try:
        lookup.lookup_entry(args.lookup)
        sys.exit()
    except AttributeError:
        pass
    try:
        lookup.lookup_entry(args.core)
        sys.exit()
    except AttributeError:
        pass


def _get_strategy(args: argparse.Namespace):
    """Return a set of decode strategies for the code to identify
    formats against.
    """
    strategy = list(decode_strategies)
    if args.nojson:
        try:
            strategy.remove(registry.DOCTYPE_JSON)
        except ValueError:
            pass
    if args.nojsonl:
        try:
            strategy.remove(registry.DOCTYPE_JSONL)
        except ValueError:
            pass
    if args.noyaml:
        try:
            strategy.remove(registry.DOCTYPE_YAML)
        except ValueError:
            pass
    if args.notoml:
        try:
            strategy.remove(registry.DOCTYPE_TOML)
        except ValueError:
            pass
    return strategy


def analysis() -> None:
    """Secondary entry point for analysis functionality.

    Enables us to call analysis from the command line once installed
    via PyPi.
    """
    parser = argparse.ArgumentParser(
        prog="jsonida",
        description="JSONID(A)nalysis",
        epilog="for more information visit https://github.com/ffdev-info/jsonid",
    )
    parser.add_argument(
        "--debug",
        help="use debug loggng",
        required=False,
        action="store_true",
    )
    parser.add_argument(
        "--path",
        "-p",
        help="analyse a file in support of ruleset development and data preservation",
        required=False,
        type=str,
        metavar="PATH",
    )
    args = parser.parse_args()

    if not args.path:
        parser.print_help(sys.stderr)
        sys.exit()

    # Initialize logging.
    init_logging(args.debug)

    # Attempt lookup in the registry. This should come first as it
    # doesn't involve reading files.
    _attempt_lookup(args)

    # Determine which decode strategy to adopt.
    strategy = _get_strategy(args)
    if not strategy:
        logger.error(
            "please ensure there is one remaining decode strategy, e.g. %s",
            ",".join(decode_strategies),
        )
        sys.exit(1)

    # Enable graceful exit via signal handler...
    def signal_handler(*args):  # pylint: disable=W0613
        logger.info("exiting...")
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    if args.path:
        asyncio.run(
            file_processing.analyse_data(
                path=args.path,
                strategy=strategy,
            )
        )


def main() -> None:
    """Primary entry point for this script."""

    # pylint: disable=R0912,R0915

    parser = argparse.ArgumentParser(
        prog="jsonid",
        description="JSON(ID)entification of objects on disk based on identifying valid objects and their key-values",
        epilog="for more information visit https://github.com/ffdev-info/jsonid",
    )
    parser.add_argument(
        "--debug",
        help="use debug loggng",
        required=False,
        action="store_true",
    )
    parser.add_argument(
        "--path",
        "--paths",
        "-p",
        help="file path to process",
        required=False,
    )
    parser.add_argument(
        "--nojson",
        "-nj",
        action="store_true",
        required=False,
    )
    parser.add_argument(
        "--nojsonl",
        "-njl",
        action="store_true",
        required=False,
    )
    parser.add_argument(
        "--noyaml",
        "-ny",
        action="store_true",
        required=False,
    )
    parser.add_argument(
        "--notoml",
        "-nt",
        action="store_true",
        required=False,
    )
    parser.add_argument(
        "--binary",
        help="report on binary formats as well as plaintext (BETA: for preliminary identification only)",
        required=False,
        action="store_true",
    )
    parser.add_argument(
        "--agentout",
        help="output results suitable for mapping to a digital preservation system",
        required=False,
        action="store_true",
    )
    parser.add_argument(
        "--registry",
        help="path to a custom registry to lead into memory replacing the default",
        required=False,
    )
    # NB. consider output to stdout once the feature is more stable.
    parser.add_argument(
        "--pronom",
        help=f"return a PRONOM-centric view of the results to `{export.PRONOM_FILENAME}` (BETA)",
        required=False,
        action="store_true",
    )
    parser.add_argument(
        "--export",
        help="export the embedded registry",
        required=False,
        action="store_true",
    )
    parser.add_argument(
        "--check",
        help="check the registry entries are correct",
        required=False,
        action="store_true",
    )
    parser.add_argument(
        "--html",
        help="output the registry as html",
        required=False,
        action="store_true",
    )
    parser.add_argument(
        "--language",
        help="return results in different languages",
        required=False,
    )
    parser.add_argument(
        "--analyse",
        "--analyze",
        "--analysis",
        "-a",
        help="analyse a file in support of ruleset development and data preservation",
        required=False,
        type=str,
        metavar="PATH",
    )
    subparsers = parser.add_subparsers(help="registry lookup functions")
    parser_core = subparsers.add_parser(
        "core", help=f"display information about core formats: {registry.REGISTERED}"
    )
    parser_core.add_argument(
        "core", choices=registry.REGISTERED, help="lookup one of the core entries"
    )
    parser_lookup = subparsers.add_parser("lookup", help="lookup all other identifiers")
    parser_lookup.add_argument(
        "lookup", type=str, help="lookup all non-core registry entries"
    )
    args = parser.parse_args()

    # Initialize logging.
    init_logging(args.debug)

    # Attempt lookup in the registry. This should come first as it
    # doesn't involve reading files.
    _attempt_lookup(args)

    # Determine which decode strategy to adopt.
    strategy = _get_strategy(args)

    # Primary application functions.
    if args.registry:
        raise NotImplementedError("custom registry is not yet available")
    if args.pronom:
        export.export_pronom()
        sys.exit()
    if args.language:
        raise NotImplementedError("multiple languages are not yet implemented")
    if args.export:
        export.exportJSON()
        sys.exit()
    if args.check:
        if not helpers.entry_check():
            logger.error("registry entries are not correct")
            sys.exit(1)
        if not helpers.keys_check():
            logger.error(
                "invalid keys appear in data (use `--debug` logging for more information)"
            )
            sys.exit(1)
        logger.info("ok")
        sys.exit()
    if args.html:
        helpers.html()
        sys.exit()
    if not strategy:
        logger.error(
            "please ensure there is one remaining decode strategy, e.g. %s",
            ",".join(decode_strategies),
        )
        sys.exit(1)
    if args.analyse:
        asyncio.run(
            file_processing.analyse_data(
                path=args.analyse,
                strategy=strategy,
            )
        )
        sys.exit()
    if not args.path:
        parser.print_help(sys.stderr)
        sys.exit()

    # Enable graceful exit via signal handler...
    def signal_handler(*args):  # pylint: disable=W0613
        logger.info("exiting...")
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    # Run JSONID.
    asyncio.run(
        file_processing.process_data(
            path=args.path,
            strategy=strategy,
            binary=args.binary,
            agentout=args.agentout,
        )
    )


if __name__ == "__main__":
    main()
