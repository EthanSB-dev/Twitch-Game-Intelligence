-- Twitch Helix Game Intelligence: initial database schema

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
    game_id TEXT REFERENCES games(game_id),
    game_name TEXT,
    title TEXT NOT NULL,
    language TEXT,
    started_at TIMESTAMPTZ NOT NULL,
    is_mature BOOLEAN NOT NULL DEFAULT FALSE,
    first_seen_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    last_seen_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS stream_snapshots (
    snapshot_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    stream_id TEXT NOT NULL REFERENCES streams(stream_id),
    game_id TEXT REFERENCES games(game_id),
    viewer_count INTEGER NOT NULL CHECK (viewer_count >= 0),
    collected_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (stream_id, collected_at)
);

CREATE INDEX IF NOT EXISTS idx_streams_game_id
    ON streams (game_id);

CREATE INDEX IF NOT EXISTS idx_stream_snapshots_stream_collected_at
    ON stream_snapshots (stream_id, collected_at DESC);

CREATE INDEX IF NOT EXISTS idx_stream_snapshots_game_collected_at
    ON stream_snapshots (game_id, collected_at DESC);