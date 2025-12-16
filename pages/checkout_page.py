"""Страница оформления заказа."""
from .base_page import BasePage


class CheckoutPage(BasePage):
    first_name_input = BasePage.by_css("#first-name")
    last_name_input = BasePage.by_css("#last-name")
    postal_code_input = BasePage.by_css("#postal-code")
    continue_button = BasePage.by_css("#continue")
    finish_button = BasePage.by_css("#finish")

    summary_total = BasePage.by_css(".summary_total_label")
    summary_subtotal = BasePage.by_css(".summary_subtotal_label")
    summary_tax = BasePage.by_css(".summary_tax_label")
    complete_header = BasePage.by_css(".complete-header")

    def fill_form(self, first: str, last: str, postal: str) -> None:
        """Заполнить форму клиента."""
        self.fill(self.first_name_input, first)
        self.fill(self.last_name_input, last)
        self.fill(self.postal_code_input, postal)

    def continue_checkout(self) -> None:
        """Перейти к итогам заказа."""
        self.click(self.continue_button)

    def finish_order(self) -> None:
        """Завершить оформление."""
        self.click(self.finish_button)

    def totals(self) -> dict:
        """Получить суммы из блока итогов."""
        subtotal = float(self.text(self.summary_subtotal).split("$")[1])
        tax = float(self.text(self.summary_tax).split("$")[1])
        total = float(self.text(self.summary_total).split("$")[1])
        return {"subtotal": subtotal, "tax": tax, "total": total}

    def is_completed(self) -> bool:
        """Проверить, что заказ завершён."""
        try:
            self.wait_visible(self.complete_header)
            return True
        except Exception:
            return False
