from contextlib import contextmanager
from typing import Iterator

import psycopg
from psycopg import Connection

from twitch_intelligence.config import Settings, load_settings


def build_connection_string(settings: Settings) -> str:
    return (
        f"host={settings.database_host} "
        f"port={settings.database_port} "
        f"dbname={settings.database_name} "
        f"user={settings.database_user} "
        f"password={settings.database_password}"
    )


@contextmanager
def get_connection() -> Iterator[Connection]:
    settings = load_settings()
    connection = psycopg.connect(build_connection_string(settings))

    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()