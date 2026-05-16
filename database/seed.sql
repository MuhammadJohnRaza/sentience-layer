INSERT INTO users (username) VALUES ('admin'), ('testuser') ON CONFLICT DO NOTHING;
INSERT INTO memories (user_id, content) VALUES (1, 'Initial memory core established.') ON CONFLICT DO NOTHING;
