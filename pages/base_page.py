"""Базовый класс Page Object с общими методами ожиданий."""
from typing import Tuple

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    """Общие методы работы со страницами."""

    def __init__(self, driver: WebDriver, timeout: int = 10) -> None:
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def open(self, url: str) -> None:
        """Открыть указанный URL."""
        self.driver.get(url)

    def find(self, locator: Tuple[str, str]):
        """Найти элемент по локатору."""
        return self.wait.until(EC.presence_of_element_located(locator))

    def click(self, locator: Tuple[str, str]) -> None:
        """Кликнуть по элементу."""
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()

    def fill(self, locator: Tuple[str, str], value: str) -> None:
        """Очистить и заполнить поле."""
        element = self.find(locator)
        element.clear()
        element.send_keys(value)

    def text(self, locator: Tuple[str, str]) -> str:
        """Получить текст элемента."""
        element = self.find(locator)
        return element.text

    def wait_visible(self, locator: Tuple[str, str]) -> None:
        """Дождаться видимости элемента."""
        self.wait.until(EC.visibility_of_element_located(locator))

    def wait_all_visible(self, locator: Tuple[str, str]) -> None:
        """Дождаться видимости всех элементов по локатору."""
        self.wait.until(EC.visibility_of_all_elements_located(locator))

    @staticmethod
    def by_css(selector: str) -> Tuple[str, str]:
        return By.CSS_SELECTOR, selector

    @staticmethod
    def by_xpath(xpath: str) -> Tuple[str, str]:
        return By.XPATH, xpath
