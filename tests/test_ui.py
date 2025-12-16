"""UI-тесты для сайта saucedemo."""
import math

import allure
import pytest

from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from data import users


pytestmark = [pytest.mark.ui]


@allure.feature("Авторизация")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Успешный вход под стандартным пользователем")
def test_login_success(driver):
    login_page = LoginPage(driver)
    inventory_page = InventoryPage(driver)

    with allure.step("Открыть страницу логина"):
        login_page.open_login()

    with allure.step("Авторизоваться корректными данными"):
        login_page.login(users.standard_user["username"], users.standard_user["password"])

    with allure.step("Дождаться загрузки каталога"):
        inventory_page.wait_loaded()

    assert "inventory" in driver.current_url, "Пользователь не попал в каталог"


@allure.feature("Авторизация")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("Ошибка при некорректном пароле")
def test_login_invalid_password(driver):
    login_page = LoginPage(driver)

    with allure.step("Открыть страницу логина"):
        login_page.open_login()

    with allure.step("Ввести неверные данные"):
        login_page.login(users.fake_user["username"], users.fake_user["password"])

    with allure.step("Проверить сообщение об ошибке"):
        error = login_page.get_error()

    assert error is not None and "Epic sadface" in error, "Ошибка авторизации не отображается"


@allure.feature("Корзина")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Добавление одного товара отражается в корзине")
def test_add_single_item(driver):
    login_page = LoginPage(driver)
    inventory_page = InventoryPage(driver)
    cart_page = CartPage(driver)

    login_page.open_login()
    login_page.login(users.standard_user["username"], users.standard_user["password"])
    inventory_page.wait_loaded()

    product = "Sauce Labs Backpack"

    with allure.step("Добавить товар в корзину"):
        price = inventory_page.item_price(product)
        inventory_page.add_to_cart(product)

    with allure.step("Проверить бейдж корзины"):
        assert inventory_page.cart_count() == 1, "Количество в корзине должно быть 1"

    with allure.step("Перейти в корзину"):
        inventory_page.open_cart()
        cart_page.wait_loaded()

    items = cart_page.items()
    assert len(items) == 1, "В корзине ожидается один товар"
    assert math.isclose(items[0][1], price, rel_tol=0, abs_tol=0.01), "Цена товара не совпадает"


@allure.feature("Корзина")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("Удаление одного из товаров из корзины")
def test_add_and_remove(driver):
    login_page = LoginPage(driver)
    inventory_page = InventoryPage(driver)
    cart_page = CartPage(driver)

    login_page.open_login()
    login_page.login(users.standard_user["username"], users.standard_user["password"])
    inventory_page.wait_loaded()

    first = "Sauce Labs Backpack"
    second = "Sauce Labs Bike Light"

    with allure.step("Добавить два товара"):
        inventory_page.add_to_cart(first)
        inventory_page.add_to_cart(second)

    inventory_page.open_cart()
    cart_page.wait_loaded()

    with allure.step("Удалить один товар"):
        cart_page.remove(second)

    remaining = [name for name, _ in cart_page.items()]
    assert remaining == [first], "В корзине должен остаться только первый товар"


@allure.feature("Оформление заказа")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Итоги заказа соответствуют сумме и налогу")
def test_checkout_totals(driver):
    login_page = LoginPage(driver)
    inventory_page = InventoryPage(driver)
    cart_page = CartPage(driver)
    checkout_page = CheckoutPage(driver)

    login_page.open_login()
    login_page.login(users.standard_user["username"], users.standard_user["password"])
    inventory_page.wait_loaded()

    first = "Sauce Labs Backpack"
    second = "Sauce Labs Bike Light"

    with allure.step("Добавить товары в корзину"):
        p1 = inventory_page.item_price(first)
        p2 = inventory_page.item_price(second)
        inventory_page.add_to_cart(first)
        inventory_page.add_to_cart(second)

    inventory_page.open_cart()
    cart_page.wait_loaded()

    with allure.step("Перейти к оформлению"):
        cart_page.proceed_checkout()

    with allure.step("Заполнить данные покупателя"):
        checkout_page.fill_form(
            users.customer["first_name"],
            users.customer["last_name"],
            users.customer["postal_code"],
        )
        checkout_page.continue_checkout()

    with allure.step("Получить суммы"):
        totals = checkout_page.totals()

    expected_subtotal = round(p1 + p2, 2)
    assert math.isclose(totals["subtotal"], expected_subtotal, abs_tol=0.01), "Неверная сумма товаров"
    assert math.isclose(totals["total"], totals["subtotal"] + totals["tax"], abs_tol=0.01), "Тотал не совпадает с суммой и налогом"

    with allure.step("Завершить заказ"):
        checkout_page.finish_order()

    assert checkout_page.is_completed(), "Заказ не завершился успешно"
