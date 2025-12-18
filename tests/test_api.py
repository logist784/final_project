"""API-тесты для публичного REST API Википедии."""
import allure
import pytest

from api.wiki_client import WikipediaClient


pytestmark = [pytest.mark.api]


@allure.feature("Статьи")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("Поиск (Action API) возвращает результаты")
def test_search_title(api_client: WikipediaClient):
    query = "Тестирование"
    with allure.step("Запросить поиск через Action API"):
        response = api_client.action_search(query, limit=10)

    with allure.step("Проверить статус и наличие результатов"):
        assert response.status_code == 200
        body = response.json()
        search = body.get("query", {}).get("search", [])
        assert isinstance(search, list) and len(search) > 0


@allure.feature("Статьи")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Получение краткого описания статьи")
def test_get_summary(api_client: WikipediaClient):
    title = "Тестирование программного обеспечения"
    with allure.step("Запросить summary статьи"):
        response = api_client.summary(title)

    with allure.step("Проверить корректность данных"):
        assert response.status_code == 200
        data = response.json()
        assert data.get("title") and title in data.get("title")
        assert data.get("extract"), "Нет краткого описания"


@allure.feature("Статьи")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Получение случайной статьи")
def test_random_summary(api_client: WikipediaClient):
    with allure.step("Запросить случайную статью"):
        response = api_client.random_summary()

    with allure.step("Проверить ответ"):
        assert response.status_code == 200
        body = response.json()
        assert body.get("title")
        assert body.get("extract")
