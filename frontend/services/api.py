import os
from typing import Any

import requests
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000").rstrip("/")

CONNECTION_ERROR = "Não foi possível conectar ao servidor. Verifique se a API está ativa e tente novamente."
HTTP_SESSION = requests.Session()


def call(method: str, path: str, token: str | None = None, raw: bool = False, **kwargs: Any) -> Any:
    headers = kwargs.pop("headers", {})
    if token:
        headers["Authorization"] = f"Bearer {token}"
    try:
        response = HTTP_SESSION.request(method, f"{API_URL}{path}", headers=headers, timeout=20, **kwargs)
    except requests.RequestException as error:
        raise RuntimeError(CONNECTION_ERROR) from error

    if response.status_code >= 400:
        try:
            detail = response.json().get("detail", "Erro na API")
        except ValueError:
            detail = response.text or "Erro na API"
        raise RuntimeError(detail)

    if raw:
        return response.content
    if not response.content:
        return None

    try:
        return response.json()
    except ValueError as error:
        raise RuntimeError("Resposta inválida da API. Verifique se o backend está disponível e acessível.") from error
