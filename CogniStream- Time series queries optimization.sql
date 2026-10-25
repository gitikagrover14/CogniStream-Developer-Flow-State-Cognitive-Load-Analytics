USE cognistream;

-- 1. Check total records
SELECT
    source,
    COUNT(*) AS total_events
FROM developer_events
GROUP BY source;

-- 2. Check the overall time range
SELECT
    MIN(event_timestamp) AS first_event,
    MAX(event_timestamp) AS last_event
FROM developer_events;

-- 3. Check developer activity
SELECT
    developer_id,
    COUNT(*) AS total_events
FROM developer_events
GROUP BY developer_id;

-- Events per hour
SELECT
    DATE_FORMAT(event_timestamp, '%Y-%m-%d %H:00:00') AS event_hour,
    COUNT(*) AS total_events
FROM developer_events
GROUP BY event_hour
ORDER BY event_hour;

-- Events by source over time
SELECT
    DATE(event_timestamp) AS event_date,
    source,
    COUNT(*) AS total_events
FROM developer_events
GROUP BY event_date, source
ORDER BY event_date, source;

-- Developer activity within a time range
SELECT
    developer_id,
    source,
    event_timestamp,
    event_type
FROM developer_events
WHERE event_timestamp >= '2020-01-01 00:00:00'
  AND event_timestamp < '2030-01-01 00:00:00'
ORDER BY event_timestamp;

SHOW INDEX FROM developer_events;

EXPLAIN
SELECT
    developer_id,
    event_timestamp,
    event_type
FROM developer_events
WHERE developer_id = 'dev_001'
ORDER BY event_timestamp;

