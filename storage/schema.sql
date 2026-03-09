-- SQLite for structured data
CREATE TABLE events (
    id INTEGER PRIMARY KEY,
    type TEXT,  -- 'git_commit', 'slack_decision', 'pr_context', etc.
    source TEXT,  -- 'git', 'slack', 'github', 'ide'
    project TEXT,  -- project/repo name
    content TEXT,  -- full text content
    metadata JSON,  -- flexible metadata
    timestamp DATETIME
    -- embedding BLOB  -- vector embedding for semantic search
);

CREATE TABLE knowledge_graph (
    id INTEGER PRIMARY KEY,
    event_id INTEGER,
    related_event_id INTEGER,
    relationship_type TEXT,  -- 'implements', 'discusses', 'blocks'
    confidence REAL,
    FOREIGN KEY (event_id) REFERENCES events(id)
);

