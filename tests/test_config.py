from pact.config import settings


def test_settings() -> None:
    assert settings.app_name == "PACT"
    assert settings.environment == "development"
    assert settings.debug is True
