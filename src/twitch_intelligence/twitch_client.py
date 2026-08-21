from __future__ import annotations

import requests

from twitch_intelligence.config import load_settings


TOKEN_URL = "https://id.twitch.tv/oauth2/token"
VALIDATE_URL = "https://id.twitch.tv/oauth2/validate"


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


def validate_token(access_token: str) -> dict:
    """Return Twitch's metadata for a valid OAuth access token."""
    response = requests.get(
        VALIDATE_URL,
        headers={"Authorization": f"OAuth {access_token}"},
        timeout=30,
    )
    response.raise_for_status()

    return response.json()