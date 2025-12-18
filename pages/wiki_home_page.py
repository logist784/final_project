from config.settings import settings
from .base_page import BasePage


class WikiHomePage(BasePage):
    url: str = settings.ui_base_url

    search_input = BasePage.by_css("#searchInput")
    search_button = BasePage.by_css("#searchButton")

    def open_home(self) -> None:
        self.open(self.url)

    def search(self, query: str) -> None:
        self.fill(self.search_input, query)
        self.click(self.search_button)

