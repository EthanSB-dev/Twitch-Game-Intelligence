from dataclasses import dataclass
import os

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    database_host: str
    database_port: int
    database_name: str
    database_user: str
    database_password: str
    twitch_client_id: str | None
    twitch_client_secret: str | None


def require_env(name: str) -> str:
    value = os.getenv(name)

    if not value:
        raise ValueError(
            f"Missing required environment variable: {name}. "
            "Add it to your local .env file."
        )

    return value


def load_settings() -> Settings:
    load_dotenv()

    return Settings(
        database_host=os.getenv("DATABASE_HOST", "localhost"),
        database_port=int(os.getenv("POSTGRES_PORT", "5433")),
        database_name=require_env("POSTGRES_DB"),
        database_user=require_env("POSTGRES_USER"),
        database_password=require_env("POSTGRES_PASSWORD"),
        twitch_client_id=os.getenv("TWITCH_CLIENT_ID") or None,
        twitch_client_secret=os.getenv("TWITCH_CLIENT_SECRET") or None,
    )