from pact.logger import get_logger
from pact.logger import LOG_FILE

def test_logger() -> None:
    logger = get_logger("test_logger")
    message = "PACT logger test"

    logger.info(message)

    for handler in logger.handlers:
        handler.flush()

    assert LOG_FILE.exists()

    assert message in LOG_FILE.read_text(encoding="utf-8")
    