"""Настройки окружения проекта."""
import os
from dataclasses import dataclass


def _as_bool(value: str | None, default: bool) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "y"}


def _as_int(value: str | None, default: int) -> int:
    try:
        return int(value) if value is not None else default
    except ValueError:
        return default


@dataclass(frozen=True)
class Settings:
    """Конфигурация приложения."""

    ui_base_url: str = os.getenv("UI_BASE_URL", "https://ru.wikipedia.org/")
    api_base_url: str = os.getenv(
        "API_BASE_URL", "https://ru.wikipedia.org/api/rest_v1"
    )
    browser: str = os.getenv("BROWSER", "chrome").lower()
    headless: bool = _as_bool(os.getenv("HEADLESS"), True)
    timeout: int = _as_int(os.getenv("TIMEOUT"), 10)


settings = Settings()
