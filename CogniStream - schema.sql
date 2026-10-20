CREATE DATABASE IF NOT EXISTS cognistream;
USE cognistream;

CREATE TABLE IF NOT EXISTS developer_events (
    event_id VARCHAR(100) PRIMARY KEY,
    developer_id VARCHAR(100) NOT NULL,
    team_id VARCHAR(100) DEFAULT 'team_a',
    source ENUM('github', 'slack', 'ide') NOT NULL,
    event_type VARCHAR(100) NOT NULL,
    event_timestamp DATETIME NOT NULL,
    repo_or_channel VARCHAR(255) DEFAULT '',
    message_or_detail TEXT,
    ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_dev_time (developer_id, event_timestamp),
    INDEX idx_source_time (source, event_timestamp)
);

INSERT INTO developer_events
(event_id, developer_id, source, event_type, event_timestamp, repo_or_channel, message_or_detail)
VALUES
('gh_001', 'dev_01', 'github', 'commit', '2026-10-20 10:00:00', 'cognistream-api', 'Initial commit'),
('sl_001', 'dev_01', 'slack', 'message', '2026-10-20 10:15:00', '#dev-alerts', 'CI/CD build failed'),
('ide_001', 'dev_01', 'ide', 'coding_session', '2026-10-20 10:20:00', 'cognistream-api', 'VSCode active session');

SELECT *
FROM developer_events
ORDER BY event_timestamp;

SELECT
    source,
    COUNT(*) AS total_events,
    MIN(event_timestamp) AS first_event,
    MAX(event_timestamp) AS last_event
FROM developer_events
GROUP BY source;

DESCRIBE developer_events;

SHOW INDEX FROM developer_events;

SELECT
    COUNT(*) AS total_events,
    COUNT(DISTINCT developer_id) AS total_developers,
    COUNT(DISTINCT source) AS total_sources
FROM developer_events;