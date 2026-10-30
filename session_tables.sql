USE cognistream;

-- Store identified coding sessions
CREATE TABLE IF NOT EXISTS coding_sessions (
    session_id INT AUTO_INCREMENT PRIMARY KEY,
    developer_id VARCHAR(100) NOT NULL,
    session_start DATETIME NOT NULL,
    session_end DATETIME NOT NULL,
    total_events INT,
    duration_minutes DECIMAL(10,2),
    potential_slack_interruptions INT DEFAULT 0,
    meets_90min_flow_criteria BOOLEAN
);

-- Store Slack messages matched with coding sessions
CREATE TABLE IF NOT EXISTS session_interruptions (
    interruption_id INT AUTO_INCREMENT PRIMARY KEY,
    session_id INT NOT NULL,
    slack_timestamp DATETIME NOT NULL,
    slack_message TEXT,
    FOREIGN KEY (session_id)
        REFERENCES coding_sessions(session_id)
);

-- Verify tables
SHOW TABLES;

DESCRIBE coding_sessions;
DESCRIBE session_interruptions;

SELECT * FROM coding_sessions;

SELECT * FROM session_interruptions;

SELECT
    COUNT(*) AS total_sessions,
    AVG(duration_minutes) AS average_duration,
    SUM(potential_slack_interruptions) AS total_interruptions
FROM coding_sessions;