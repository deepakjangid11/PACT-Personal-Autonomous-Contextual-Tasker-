import sys

from pact.exception import CustomException


def test_custom_exception() -> None:
    try:
        raise ValueError("Test error")
    except Exception as e:
        error = CustomException(e, sys)

        assert "Test error" in str(error)
        assert "test_exception.py" in str(error)