import sys
from pact.exception import CustomException
from pact.logger import get_logger
logger = get_logger(__name__)


def main() -> None:
    try:
        logger.info("PACT application started")

    except Exception as e:
        raise CustomException(e, sys)


if __name__ == "__main__":
    main()