CREATE TABLE IF NOT EXISTS games (
    game_id TEXT PRIMARY KEY,
    game_name TEXT NOT NULL,
    box_art_url TEXT,
    first_seen_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    last_seen_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS streams (
    stream_id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    user_login TEXT NOT NULL,
    user_name TEXT NOT NULL,
    game_id TEXT REFERENCES games (game_id),
    title TEXT NOT NULL,
    language TEXT,
    started_at TIMESTAMPTZ NOT NULL,
    first_seen_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    last_seen_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS stream_snapshots (
    stream_id TEXT NOT NULL REFERENCES streams (stream_id) ON DELETE CASCADE,
    collected_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    viewer_count INTEGER NOT NULL CHECK (viewer_count >= 0),
    PRIMARY KEY (stream_id, collected_at)
);

CREATE INDEX IF NOT EXISTS idx_streams_game_id
    ON streams (game_id);

CREATE INDEX IF NOT EXISTS idx_stream_snapshots_collected_at
    ON stream_snapshots (collected_at);

CREATE INDEX IF NOT EXISTS idx_stream_snapshots_stream_collected
    ON stream_snapshots (stream_id, collected_at);