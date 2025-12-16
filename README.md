# Финальный проект: UI и API автотесты

Набор из 5 UI и 5 API автотестов на публичных стендах saucedemo (UI) и jsonplaceholder.typicode.com (API). Используется Page Object для UI и клиент-обёртка для API, отчётность в Allure.

## Стек
- Python 3.10+
- pytest
- selenium + webdriver-manager
- requests
- allure-pytest

## Структура
```
final_project/
  api/                # Клиент reqres
  config/             # Настройки окружения
  data/               # Тестовые данные
  pages/              # Page Object для UI
  tests/              # UI и API тесты + фикстуры
  pytest.ini          # Маркеры ui/api
  requirements.txt    # Зависимости
```

## Подготовка
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## Запуск
- Все тесты: `pytest tests -m "ui or api"`
- Только UI: `pytest tests -m ui`
- Только API: `pytest tests -m api`

### Allure
```bash
pytest tests -m "ui or api" --alluredir=allure-results
allure serve allure-results
```

## Настройки окружения
- `BROWSER` — chrome | firefox (по умолчанию chrome)
- `HEADLESS` — 1/0 для безголового режима (по умолчанию 1)
- `UI_BASE_URL` — базовый URL UI (по умолчанию https://www.saucedemo.com/)
- `API_BASE_URL` — базовый URL API (по умолчанию https://jsonplaceholder.typicode.com)
- `TIMEOUT` — таймаут ожиданий Selenium в секундах (по умолчанию 10)

## Примечания
- Данные авторизации, URL и тестовые payload вынесены в `data/` и `config/`.
- Папки с отчётами и кэшем исключены в `.gitignore`.
- Проект соответствует PEP8 и требованиям финального задания.
