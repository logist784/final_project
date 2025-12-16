"""Страница корзины."""
from typing import List, Tuple

from .base_page import BasePage


class CartPage(BasePage):
    cart_list = BasePage.by_css(".cart_list")
    checkout_button = BasePage.by_css("#checkout")

    def wait_loaded(self) -> None:
        """Дождаться загрузки корзины."""
        self.wait_visible(self.cart_list)

    def _item_row(self, name: str) -> str:
        return f"//div[@class='cart_item' and .//div[text()='{name}']]"

    def remove(self, name: str) -> None:
        """Удалить товар из корзины по названию."""
        remove_btn = self.by_xpath(self._item_row(name) + "//button")
        self.click(remove_btn)

    def items(self) -> List[Tuple[str, float]]:
        """Получить список (название, цена) товаров в корзине."""
        row_locator = self.by_css(".cart_item")
        rows = self.wait.until(lambda d: d.find_elements(*row_locator))
        result = []
        for row in rows:
            name = row.find_element(*self.by_css(".inventory_item_name")).text
            price_text = row.find_element(
                *self.by_css(".inventory_item_price")
            ).text.replace("$", "")
            result.append((name, float(price_text)))
        return result

    def proceed_checkout(self) -> None:
        """Нажать Checkout."""
        self.click(self.checkout_button)
