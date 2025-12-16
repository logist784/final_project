"""API-тесты для публичного сервиса jsonplaceholder.typicode.com."""
import allure
import pytest

from api.client import JsonPlaceholderClient
from data import api_data


pytestmark = [pytest.mark.api]


@allure.feature("Посты")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("Получение списка постов")
def test_list_posts(api_client: JsonPlaceholderClient):
    with allure.step("Запросить список постов"):
        response = api_client.list_posts()

    with allure.step("Проверить статус и наличие элементов"):
        assert response.status_code == 200
        body = response.json()
        assert isinstance(body, list) and len(body) >= 100, "Список постов пуст или укорочен"


@allure.feature("Посты")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Получение поста по id")
def test_get_post(api_client: JsonPlaceholderClient):
    post_id = 1
    with allure.step("Запросить пост по id"):
        response = api_client.get_post(post_id)

    with allure.step("Проверить корректность данных"):
        assert response.status_code == 200
        data = response.json()
        assert data.get("id") == post_id, "ID поста не совпадает"
        assert data.get("title"), "Нет заголовка"
        assert data.get("body"), "Нет текста"


@allure.feature("Посты")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Создание поста")
def test_create_post(api_client: JsonPlaceholderClient):
    with allure.step("Создать пост"):
        response = api_client.create_post(api_data.create_post_payload)

    with allure.step("Проверить ответ"):
        assert response.status_code == 201
        body = response.json()
        assert body.get("title") == api_data.create_post_payload["title"]
        assert body.get("body") == api_data.create_post_payload["body"]
        assert body.get("id"), "В ответе нет id"


@allure.feature("Посты")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("Обновление поста")
def test_update_post(api_client: JsonPlaceholderClient):
    with allure.step("Обновить пост"):
        response = api_client.update_post(1, api_data.update_post_payload)

    with allure.step("Проверить обновлённые поля"):
        assert response.status_code == 200
        body = response.json()
        assert body.get("title") == api_data.update_post_payload["title"]
        assert body.get("body") == api_data.update_post_payload["body"]


@allure.feature("Посты")
@allure.severity(allure.severity_level.MINOR)
@allure.title("Удаление поста")
def test_delete_post(api_client: JsonPlaceholderClient):
    with allure.step("Удалить пост"):
        response = api_client.delete_post(1)

    with allure.step("Проверить код ответа"):
        assert response.status_code in (200, 204)
