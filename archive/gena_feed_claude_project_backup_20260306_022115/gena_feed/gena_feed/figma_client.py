from __future__ import annotations

import os
from typing import Any

import requests
from dotenv import load_dotenv


class FigmaApiError(RuntimeError):
    """Raised for Figma API failures."""


class FigmaClient:
    """Thin Figma REST API client."""

    BASE_URL = "https://api.figma.com/v1"

    def __init__(
        self,
        access_token: str | None = None,
        file_id: str | None = None,
        *,
        timeout: int = 30,
        load_environment: bool = True,
    ) -> None:
        if load_environment:
            load_dotenv()

        self.access_token = (access_token or os.getenv("FIGMA_ACCESS_TOKEN", "")).strip()
        self.file_id = (file_id or os.getenv("FIGMA_FILE_ID") or os.getenv("FIGMA_FILE_KEY", "")).strip()
        self.timeout = timeout

        if not self.access_token:
            raise ValueError("FIGMA_ACCESS_TOKEN not found in environment")
        if not self.file_id:
            raise ValueError("FIGMA_FILE_ID (or FIGMA_FILE_KEY) not found in environment")

        self.headers = {
            "X-Figma-Token": self.access_token,
            "Content-Type": "application/json",
        }

    def _request(self, method: str, endpoint: str, **kwargs: Any) -> dict[str, Any]:
        path = endpoint if endpoint.startswith("/") else f"/{endpoint}"
        url = f"{self.BASE_URL}{path}"
        try:
            response = requests.request(
                method=method.upper(),
                url=url,
                headers=self.headers,
                timeout=self.timeout,
                **kwargs,
            )
        except requests.RequestException as exc:
            raise FigmaApiError(f"Request failed: {url} ({exc})") from exc

        if response.status_code >= 400:
            message = response.text[:300]
            try:
                payload = response.json()
                message = payload.get("err") or payload.get("message") or message
            except ValueError:
                pass
            raise FigmaApiError(f"Figma API error {response.status_code}: {message}")

        try:
            return response.json()
        except ValueError as exc:
            raise FigmaApiError(f"Invalid JSON response from {url}") from exc

    def get_file(self, file_id: str | None = None) -> dict[str, Any]:
        fid = (file_id or self.file_id).strip()
        return self._request("GET", f"/files/{fid}")

    def get_file_nodes(self, node_ids: list[str], file_id: str | None = None) -> dict[str, Any]:
        if not node_ids:
            raise ValueError("node_ids is empty")
        fid = (file_id or self.file_id).strip()
        return self._request("GET", f"/files/{fid}/nodes", params={"ids": ",".join(node_ids)})

    def get_images(
        self,
        node_ids: list[str],
        *,
        scale: float = 2.0,
        format: str = "png",
        file_id: str | None = None,
    ) -> dict[str, Any]:
        if not node_ids:
            raise ValueError("node_ids is empty")
        fid = (file_id or self.file_id).strip()
        fmt = format.lower().strip()
        if fmt not in {"png", "jpg", "svg", "pdf"}:
            raise ValueError(f"Unsupported format: {format}")
        params = {"ids": ",".join(node_ids), "scale": scale, "format": fmt}
        return self._request("GET", f"/images/{fid}", params=params)

    def test_connection(self) -> bool:
        try:
            self._request("GET", "/me")
            return True
        except FigmaApiError:
            return False
