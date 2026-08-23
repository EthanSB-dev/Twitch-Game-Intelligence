from __future__ import annotations

from typing import Any

import requests

from twitch_intelligence.config import load_settings


TOKEN_URL = "https://id.twitch.tv/oauth2/token"
VALIDATE_URL = "https://id.twitch.tv/oauth2/validate"
HELIX_BASE_URL = "https://api.twitch.tv/helix"


def get_app_access_token() -> str:
    """Request an app access token using the client-credentials flow."""
    settings = load_settings()

    response = requests.post(
        TOKEN_URL,
        data={
            "client_id": settings.twitch_client_id,
            "client_secret": settings.twitch_client_secret,
            "grant_type": "client_credentials",
        },
        timeout=30,
    )
    response.raise_for_status()

    return response.json()["access_token"]


def validate_token(access_token: str) -> dict[str, Any]:
    """Return Twitch's metadata for a valid OAuth access token."""
    response = requests.get(
        VALIDATE_URL,
        headers={"Authorization": f"OAuth {access_token}"},
        timeout=30,
    )
    response.raise_for_status()

    return response.json()


class TwitchHelixClient:
    """Small authenticated client for Twitch Helix API requests."""

    def __init__(self) -> None:
        settings = load_settings()
        self.client_id = settings.twitch_client_id
        self.access_token = get_app_access_token()

    @property
    def headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Client-Id": self.client_id,
        }

    def get(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        response = requests.get(
            f"{HELIX_BASE_URL}{path}",
            headers=self.headers,
            params=params,
            timeout=30,
        )
        response.raise_for_status()
        return response.json()

    def get_streams(
        self,
        *,
        first: int = 20,
        game_id: str | None = None,
        language: str | None = None,
    ) -> dict[str, Any]:
        """Get current live streams, ranked by viewer count."""
        if not 1 <= first <= 100:
            raise ValueError("first must be between 1 and 100")

        params: dict[str, Any] = {"first": first}

        if game_id:
            params["game_id"] = game_id
        if language:
            params["language"] = language

        return self.get("/streams", params=params)