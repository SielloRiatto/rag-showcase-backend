from src.config import get_settings
from src.main import create_app


def test_create_app():
    app = create_app()

    assert app.title == get_settings().app_name


def test_settings_defaults():
    settings = get_settings()

    assert settings.app_name == "RAG Demo"
    assert settings.debug is False
