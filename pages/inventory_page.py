"""Страница каталога товаров."""
from typing import List

from .base_page import BasePage


class InventoryPage(BasePage):
    inventory_container = BasePage.by_css(".inventory_list")
    cart_link = BasePage.by_css(".shopping_cart_link")
    cart_badge = BasePage.by_css(".shopping_cart_badge")

    def wait_loaded(self) -> None:
        """Дождаться загрузки каталога."""
        self.wait_visible(self.inventory_container)

    def _item_block(self, name: str) -> str:
        return (
            f"//div[@class='inventory_item' and .//div[text()='{name}']]"
        )

    def add_to_cart(self, name: str) -> None:
        """Добавить товар в корзину по названию."""
        button = self.by_xpath(self._item_block(name) + "//button")
        self.click(button)

    def remove_from_cart(self, name: str) -> None:
        """Удалить товар из корзины по названию."""
        button = self.by_xpath(self._item_block(name) + "//button")
        self.click(button)

    def open_cart(self) -> None:
        """Перейти в корзину."""
        self.click(self.cart_link)

    def item_price(self, name: str) -> float:
        """Получить цену товара из каталога."""
        price_locator = self.by_xpath(
            self._item_block(name) + "//div[@class='inventory_item_price']"
        )
        price_text = self.text(price_locator).replace("$", "")
        return float(price_text)

    def cart_count(self) -> int:
        """Получить число товаров в бейдже корзины."""
        try:
            badge_text = self.text(self.cart_badge)
            return int(badge_text)
        except Exception:
            return 0

    def listed_items(self) -> List[str]:
        """Вернуть список названий товаров на странице."""
        locator = self.by_css(".inventory_item_name")
        elements = self.wait.until(
            lambda d: d.find_elements(*locator)
        )
        return [el.text for el in elements]
