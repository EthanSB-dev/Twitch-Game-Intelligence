from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from twitch_intelligence.twitch_client import TwitchHelixClient


RAW_DATA_DIR = Path("data/raw")


def export_streams_raw(first: int = 100) -> Path:
    """Fetch a Twitch streams response and save it unchanged with ingestion metadata."""
    if not 1 <= first <= 100:
        raise ValueError("first must be between 1 and 100")

    collected_at = datetime.now(timezone.utc)
    response = TwitchHelixClient().get_streams(first=first)

    payload = {
        "source": "twitch_helix_streams",
        "collected_at": collected_at.isoformat(),
        "run_id": str(uuid4()),
        "response": response,
    }

    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

    filename = f"streams_{collected_at.strftime('%Y%m%dT%H%M%SZ')}.json"
    output_path = RAW_DATA_DIR / filename

    output_path.write_text(json.dumps(payload), encoding="utf-8")

    return output_path


if __name__ == "__main__":
    saved_path = export_streams_raw()
    print(f"Saved raw Twitch payload to {saved_path}")