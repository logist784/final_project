"""UI-тесты для ru.wikipedia.org."""
import allure
import pytest

from pages.wiki_home_page import WikiHomePage
from pages.wiki_article_page import WikiArticlePage


pytestmark = [pytest.mark.ui]


@allure.feature("Поиск")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Поиск статьи и проверка заголовка")
def test_search_article_title(driver):
    home = WikiHomePage(driver)
    article = WikiArticlePage(driver)

    with allure.step("Открыть главную страницу Википедии"):
        home.open_home()

    query = "Тестирование программного обеспечения"
    with allure.step(f"Выполнить поиск по запросу: {query}"):
        home.search(query)

    with allure.step("Дождаться загрузки статьи"):
        article.wait_loaded()

    with allure.step("Проверить заголовок"):
        assert query in article.title_text()


@allure.feature("Навигация")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("Наличие оглавления на странице статьи")
def test_article_has_toc(driver):
    home = WikiHomePage(driver)
    article = WikiArticlePage(driver)

    home.open_home()
    home.search("Тестирование программного обеспечения")

    article.wait_loaded()
    assert article.has_toc(), "Оглавление статьи не найдено"
