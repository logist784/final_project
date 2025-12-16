"""Клиент для работы с публичным API jsonplaceholder.typicode.com."""
from typing import Any, Dict, Optional

import requests

from config.settings import settings


class JsonPlaceholderClient:
    """Простой клиент JSONPlaceholder."""

    def __init__(self, session: Optional[requests.Session] = None) -> None:
        self.session = session or requests.Session()
        self.base_url = settings.api_base_url.rstrip("/")

    def _url(self, path: str) -> str:
        return f"{self.base_url}/{path.lstrip('/')}"

    def list_posts(self) -> requests.Response:
        return self.session.get(self._url("posts"))

    def get_post(self, post_id: int) -> requests.Response:
        return self.session.get(self._url(f"posts/{post_id}"))

    def create_post(self, payload: Dict[str, Any]) -> requests.Response:
        return self.session.post(self._url("posts"), json=payload)

    def update_post(self, post_id: int, payload: Dict[str, Any]) -> requests.Response:
        return self.session.put(self._url(f"posts/{post_id}"), json=payload)

    def delete_post(self, post_id: int) -> requests.Response:
        return self.session.delete(self._url(f"posts/{post_id}"))
