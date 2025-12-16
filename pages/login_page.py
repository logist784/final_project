"""Страница авторизации saucedemo."""
from typing import Optional

from config.settings import settings
from .base_page import BasePage


class LoginPage(BasePage):
    url: str = settings.ui_base_url

    username_input = BasePage.by_css("#user-name")
    password_input = BasePage.by_css("#password")
    login_button = BasePage.by_css("#login-button")
    error_box = BasePage.by_css("h3[data-test='error']")

    def open_login(self) -> None:
        """Открыть страницу логина."""
        self.open(self.url)

    def login(self, username: str, password: str) -> None:
        """Выполнить вход с указанными данными."""
        self.fill(self.username_input, username)
        self.fill(self.password_input, password)
        self.click(self.login_button)

    def get_error(self) -> Optional[str]:
        """Получить текст ошибки, если отображается."""
        try:
            self.wait_visible(self.error_box)
            return self.text(self.error_box)
        except Exception:
            return None
