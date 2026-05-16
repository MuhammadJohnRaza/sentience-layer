-- Up
CREATE TABLE IF NOT EXISTS causal_links (
    id SERIAL PRIMARY KEY,
    cause TEXT,
    effect TEXT,
    confidence FLOAT
);
-- Down
DROP TABLE IF EXISTS causal_links;
