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
    import registry
except ModuleNotFoundError:
    try:
        from src.jsonid import export, file_processing, helpers, registry
    except ModuleNotFoundError:
        from jsonid import export, file_processing, helpers, registry


logger = None


decode_strategies: Final[list] = [
    registry.DOCTYPE_JSON,
    registry.DOCTYPE_JSONL,
    registry.DOCTYPE_YAML,
    registry.DOCTYPE_TOML,
]


def init_logging(debug):
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


def _get_strategy(args: argparse.Namespace):
    """Return a set of decode strategies for the code to identify
    formats against.
    """

    # pylint: disable=W0613
    def signal_handler(*args):
        logger.info("gracefully exiting...")
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

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


def main() -> None:
    """Primary entry point for this script."""

    # pylint: disable=R0912,R0915

    parser = argparse.ArgumentParser(
        prog="json-id",
        description="proof-of-concept identifier for JSON objects on disk based on identifying valid objects and their key-values",
        epilog="for more information visit https://github.com/ffdev-info/json-id",
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
        help="report on binary formats as well as plaintext",
        required=False,
        action="store_true",
    )
    parser.add_argument(
        "--simple",
        help="provide a simple single-line (JSONL) output",
        required=False,
        action="store_true",
    )
    parser.add_argument(
        "--registry",
        help="path to a custom registry to lead into memory replacing the default",
        required=False,
    )
    parser.add_argument(
        "--pronom",
        help="return a PRONOM-centric view of the results",
        required=False,
    )
    parser.add_argument(
        "--export",
        help="export the embedded registry",
        required=False,
        action="store_true",
    )
    parser.add_argument(
        "--check",
        help="check the registry entrues are correct",
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
        "-a",
        help="analyse a file in support of ruleset development and data preservation",
        required=False,
        type=str,
        metavar="PATH",
    )
    args = parser.parse_args()
    init_logging(args.debug)
    # Determine which decode strategy to adopt.
    strategy = _get_strategy(args)
    # Primary application functions.
    if args.registry:
        raise NotImplementedError("custom registry is not yet available")
    if args.pronom:
        raise NotImplementedError("pronom view is not yet implemented")
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
    asyncio.run(
        file_processing.process_data(
            path=args.path,
            strategy=strategy,
            binary=args.binary,
            simple=args.simple,
        )
    )


if __name__ == "__main__":
    main()
