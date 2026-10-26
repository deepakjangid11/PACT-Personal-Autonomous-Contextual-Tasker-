from pact.config import settings
from pact.logger import get_logger
logger = get_logger(__name__)

def start_application() -> None:
    logger.info(
        "%s application started | environment=%s",
        settings.app_name,
        settings.environment,
    )


def shutdown_applicaiton() -> None:
    logger.info(
        "%s application shutting down",
        settings.app_name,
    )

if __name__ == "__main__":
    start_application()