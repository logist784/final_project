from typing import Optional

import requests

from config.settings import settings


class WikipediaClient:
    def __init__(self, session: Optional[requests.Session] = None) -> None:
        self.session = session or requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "final_project_tests/1.0 (+https://ru.wikipedia.org/; test suite)",
                "Accept": "application/json",
            }
        )
        self.base_url = settings.api_base_url.rstrip("/")

    def _url(self, path: str) -> str:
        return f"{self.base_url}/{path.lstrip('/')}"

    def summary(self, title: str) -> requests.Response:
        return self.session.get(self._url(f"page/summary/{title}"))

    def random_summary(self) -> requests.Response:
        return self.session.get(self._url("page/random/summary"))

    def search_title(self, query: str, limit: int = 5) -> requests.Response:
        return self.session.get(self._url("search/page"), params={"q": query, "limit": limit})

    def action_search(self, query: str, limit: int = 10) -> requests.Response:
        url = "https://ru.wikipedia.org/w/api.php"
        return self.session.get(url, params={"action": "query", "list": "search", "srsearch": query, "format": "json", "srlimit": limit})
