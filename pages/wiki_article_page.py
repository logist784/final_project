from .base_page import BasePage


class WikiArticlePage(BasePage):
    heading = BasePage.by_css("#firstHeading")
    content = BasePage.by_css("#mw-content-text")
    toc = BasePage.by_css("#toc")

    def title_text(self) -> str:
        return self.text(self.heading)

    def wait_loaded(self) -> None:
        self.wait_visible(self.heading)
        self.wait_visible(self.content)

    def has_toc(self) -> bool:
        try:
            self.wait_visible(self.toc)
            return True
        except Exception:
            return False

