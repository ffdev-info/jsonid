"""Python template repository.

Baseline template for future Python code related to this project.

Replace this docstring and code below with your own code as required.
"""

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

    logger.info(
        "hello world!"
    )  # logging is lowercase, and in other cases should be informative.


if __name__ == "__main__":
    main()
