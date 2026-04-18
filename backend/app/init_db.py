import sqlite3

from app.shared.config import settings

conn = sqlite3.connect(settings.database_name)
cursor = conn.cursor()


# Create sessions table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS sessions (
        id TEXT PRIMARY KEY,
        title TEXT,
        status TEXT NOT NULL,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    )
""")


# Create ideas table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS ideas (
        id TEXT PRIMARY KEY,
        session_id TEXT NOT NULL,
        content TEXT NOT NULL,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        FOREIGN KEY (session_id) REFERENCES sessions(id)
    )
""")


# Create idea_variants table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS idea_variants (
        id TEXT PRIMARY KEY,
        idea_id TEXT NOT NULL,
        label TEXT,
        content TEXT NOT NULL,
        origin_type TEXT NOT NULL CHECK (origin_type IN ('mock', 'ai', 'manual')),
        is_selected INTEGER NOT NULL,
        created_at TEXT NOT NULL,
        FOREIGN KEY (idea_id) REFERENCES ideas(id)
    )
""")


# Create idea_versions table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS idea_versions (
        id TEXT PRIMARY KEY,
        session_id TEXT NOT NULL,
        source_variant_id TEXT,
        parent_version_id TEXT,
        version_number INTEGER NOT NULL,
        title TEXT,
        content TEXT NOT NULL,
        status TEXT NOT NULL,
        transformation_type TEXT,
        is_active INTEGER NOT NULL,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        FOREIGN KEY (session_id) REFERENCES sessions(id),
        FOREIGN KEY (source_variant_id) REFERENCES idea_variants(id),
        FOREIGN KEY (parent_version_id) REFERENCES idea_versions(id)
    )
""")


# Ensure only one active version per session
cursor.execute("""
    CREATE UNIQUE INDEX IF NOT EXISTS idx_active_version_per_session
    ON idea_versions (session_id)
    WHERE is_active = 1
""")


# Create version_analyses table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS version_analyses (
        id TEXT PRIMARY KEY,
        version_id TEXT NOT NULL,
        analysis_type TEXT NOT NULL,
        title TEXT,
        content TEXT NOT NULL,
        origin_type TEXT NOT NULL CHECK (origin_type IN ('mock', 'ai', 'manual')),
        created_at TEXT NOT NULL,
        FOREIGN KEY (version_id) REFERENCES idea_versions(id)
    )
""")


# Create version_comparisons table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS version_comparisons (
        id TEXT PRIMARY KEY,
        session_id TEXT NOT NULL,
        base_version_id TEXT NOT NULL,
        compared_version_id TEXT NOT NULL,
        comparison_type TEXT NOT NULL,
        summary TEXT NOT NULL,
        created_at TEXT NOT NULL,
        FOREIGN KEY (session_id) REFERENCES sessions(id),
        FOREIGN KEY (base_version_id) REFERENCES idea_versions(id),
        FOREIGN KEY (compared_version_id) REFERENCES idea_versions(id)
    )
""")


# Trigger to ensure base_version_id and compared_version_id are distinct
cursor.execute("""
    CREATE TRIGGER IF NOT EXISTS trg_distinct_versions
    BEFORE INSERT ON version_comparisons
    FOR EACH ROW
    BEGIN
        SELECT
        CASE
            WHEN NEW.base_version_id = NEW.compared_version_id THEN
                RAISE (ABORT, 'A comparison must involve two distinct versions.')
        END;
    END;
""")


# Create final_syntheses table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS final_syntheses (
        id TEXT PRIMARY KEY,
        session_id TEXT NOT NULL,
        source_version_id TEXT,
        title TEXT,
        content TEXT NOT NULL,
        origin_type TEXT NOT NULL CHECK (origin_type IN ('mock', 'ai', 'manual')),
        created_at TEXT NOT NULL,
        FOREIGN KEY (session_id) REFERENCES sessions(id),
        FOREIGN KEY (source_version_id) REFERENCES idea_versions(id)
    )
""")


conn.commit()
conn.close()
