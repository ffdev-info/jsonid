"""Python template repository.

Baseline template for future Python code related to this project.

Replace this docstring and code below with your own code as required.
"""

import argparse
import logging
import time

# Set up logging.
logging.basicConfig(
    format="%(asctime)-15s %(levelname)s :: %(filename)s:%(lineno)s:%(funcName)s() :: %(message)s",  # noqa: E501
    datefmt="%Y-%m-%d %H:%M:%S",
    level="INFO",
    handlers=[
        logging.StreamHandler(),
    ],
)

# Format logs using UTC time.
logging.Formatter.converter = time.gmtime


logger = logging.getLogger(__name__)


def main() -> None:
    """Primary entry point for this script."""

    parser = argparse.ArgumentParser(
        prog="json-vorhids",
        description="proof-of-concept identifier for JSON objects on disk based on identifying valid objects and their key-values",
        epilog="for more information visit https://github.com/ffdev-info/json-vorhIDS",
    )
    parser.add_argument(
        "--debug",
        help="use debug loggng",
        required=False,
        action="store_true",
    )

    args = parser.parse_args()
    logging.getLogger(__name__).setLevel(
        logging.DEBUG if args.debug else logging.WARNING
    )
    logger.debug("debug logging is configured")


if __name__ == "__main__":
    main()
