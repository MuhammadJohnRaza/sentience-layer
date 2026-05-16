-- Up
CREATE TABLE IF NOT EXISTS memory_nodes (
    id SERIAL PRIMARY KEY,
    label VARCHAR(50),
    attributes JSONB
);
-- Down
DROP TABLE IF EXISTS memory_nodes;
