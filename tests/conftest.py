"""Общие фикстуры для тестов."""
import sys
from pathlib import Path

import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from config.settings import settings
from api.wiki_client import WikipediaClient


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption("--browser", action="store", default=settings.browser)


@pytest.fixture(scope="session")
def app_settings():
    """Настройки окружения."""
    return settings


@pytest.fixture(scope="function")
def driver(request: pytest.FixtureRequest, app_settings):
    """Фикстура браузера с выбором движка."""
    browser = (request.config.getoption("--browser") or app_settings.browser).lower()
    headless = app_settings.headless

    if browser == "chrome":
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        try:
            service = ChromeService(ChromeDriverManager().install())
            with allure.step("Запуск Chrome"):
                drv = webdriver.Chrome(service=service, options=options)
        except Exception as e:
            pytest.skip(f"Не удалось установить ChromeDriver: {e}")
    elif browser == "firefox":
        options = FirefoxOptions()
        if headless:
            options.add_argument("-headless")
        service = FirefoxService(GeckoDriverManager().install())
        with allure.step("Запуск Firefox"):
            drv = webdriver.Firefox(service=service, options=options)
    else:
        raise pytest.UsageError("Поддерживаются только chrome или firefox")

    drv.set_window_size(1440, 900)
    drv.implicitly_wait(2)
    yield drv
    drv.quit()


@pytest.fixture(scope="session")
def api_client() -> WikipediaClient:
    """Клиент REST Wikipedia с общей сессией."""
    return WikipediaClient()
