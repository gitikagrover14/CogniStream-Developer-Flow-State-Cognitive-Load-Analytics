USE cognistream;

CREATE TABLE IF NOT EXISTS github_clean (
    commit_id VARCHAR(100) PRIMARY KEY,
    author_name VARCHAR(255),
    commit_timestamp DATETIME NULL,
    commit_message TEXT
);

CREATE TABLE IF NOT EXISTS slack_clean (
    record_id INT PRIMARY KEY,
    user_id INT,
    title TEXT,
    body TEXT,
    source VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS ide_clean (
    record_id INT PRIMARY KEY,
    user_id INT,
    title TEXT,
    completed BOOLEAN,
    source VARCHAR(50)
);

USE cognistream;

DROP TABLE IF EXISTS github_clean;
DROP TABLE IF EXISTS slack_clean;
DROP TABLE IF EXISTS ide_clean;

-- 1. GitHub cleaned data
CREATE TABLE github_clean (
    commit_id VARCHAR(100) PRIMARY KEY,
    author_name VARCHAR(255),
    commit_timestamp VARCHAR(50),
    commit_message TEXT
);

-- 2. Slack cleaned data
CREATE TABLE slack_clean (
    user_id INT,
    record_id INT PRIMARY KEY,
    title TEXT,
    body TEXT,
    source VARCHAR(50)
);

-- 3. IDE cleaned data
CREATE TABLE ide_clean (
    user_id INT,
    record_id INT PRIMARY KEY,
    title TEXT,
    completed VARCHAR(10),
    source VARCHAR(50)
);

select * from slack_clean;

USE cognistream;

SELECT 'GitHub' AS source, COUNT(*) AS total_records
FROM github_clean

UNION ALL

SELECT 'Slack', COUNT(*)
FROM slack_clean

UNION ALL

SELECT 'IDE', COUNT(*)
FROM ide_clean;

SELECT
    COUNT(*) AS total_records,
    COUNT(DISTINCT commit_id) AS unique_records
FROM github_clean;

SELECT
    COUNT(*) AS total_records,
    COUNT(DISTINCT record_id) AS unique_records
FROM slack_clean;

SELECT 
    COUNT(*) AS total_records,
    COUNT(DISTINCT record_id) AS unique_records
FROM
    ide_clean;

SELECT
    COUNT(*) AS total_records,
    COUNT(commit_timestamp) AS valid_timestamps
FROM github_clean;

SELECT * FROM github_clean LIMIT 5;

SELECT * FROM slack_clean LIMIT 5;

SELECT * FROM ide_clean LIMIT 5;

