import polars as pl
import mysql.connector

from datetime import datetime


# =====================================================
# 1. CHECK EXISTING CLEANED DATASETS
# =====================================================

print("\n========== DATASET INSPECTION ==========")

ide_path = "data/processed/ide_clean.csv"
slack_path = "data/processed/slack_clean.csv"

ide_csv = pl.read_csv(ide_path)
slack_csv = pl.read_csv(slack_path)

print("\nIDE Dataset:")
print(ide_csv.head())

print("\nSlack Dataset:")
print(slack_csv.head())

print("\nIDE Columns:", ide_csv.columns)
print("Slack Columns:", slack_csv.columns)

if "event_timestamp" not in ide_csv.columns:
    print("\nIDE dataset does not contain actual timestamps.")

if "slack_timestamp" not in slack_csv.columns:
    print("Slack dataset does not contain actual timestamps.")

print("\nUsing synthetic timestamped data for pipeline testing.")


# =====================================================
# 2. SAMPLE IDE ACTIVITY DATA
# =====================================================

ide_df = pl.DataFrame({
    "user_id": [1] * 11,

    "event_timestamp": [
        datetime(2026, 10, 27, 9, 0),
        datetime(2026, 10, 27, 9, 10),
        datetime(2026, 10, 27, 9, 20),
        datetime(2026, 10, 27, 9, 30),
        datetime(2026, 10, 27, 9, 40),
        datetime(2026, 10, 27, 9, 50),
        datetime(2026, 10, 27, 10, 0),
        datetime(2026, 10, 27, 10, 10),
        datetime(2026, 10, 27, 10, 20),
        datetime(2026, 10, 27, 10, 30),
        datetime(2026, 10, 27, 10, 40),
    ]
})


# =====================================================
# 3. IDENTIFY CODING SESSIONS USING POLARS
# =====================================================

ide_df = ide_df.sort(["user_id", "event_timestamp"])

ide_df = ide_df.with_columns(
    pl.col("event_timestamp")
    .diff()
    .over("user_id")
    .alias("time_gap")
)

ide_df = ide_df.with_columns(
    (
        pl.col("time_gap").is_null()
        | (pl.col("time_gap") > pl.duration(minutes=15))
    )
    .cast(pl.Int64)
    .alias("new_session")
)

ide_df = ide_df.with_columns(
    pl.col("new_session")
    .cum_sum()
    .over("user_id")
    .alias("session_id")
)


sessions = (
    ide_df.group_by(["user_id", "session_id"])
    .agg([
        pl.col("event_timestamp").min().alias("session_start"),
        pl.col("event_timestamp").max().alias("session_end"),
        pl.len().alias("total_events"),
    ])
    .sort(["user_id", "session_id"])
)

sessions = sessions.with_columns(
    (
        pl.col("session_end") - pl.col("session_start")
    ).dt.total_minutes().alias("duration_minutes")
)

print("\n========== CODING SESSIONS ==========")
print(sessions)


# =====================================================
# 4. SAMPLE SLACK MESSAGE DATA
# =====================================================

slack_df = pl.DataFrame({

    "user_id": [1, 1, 1, 1],

    "slack_timestamp": [
        datetime(2026, 10, 27, 9, 20),
        datetime(2026, 10, 27, 9, 50),
        datetime(2026, 10, 27, 10, 10),
        datetime(2026, 10, 27, 11, 30),
    ],

    "message": [
        "Build notification",
        "Team update",
        "Code review request",
        "Daily update",
    ]
})


# =====================================================
# 5. MATCH SLACK MESSAGES WITH CODING SESSIONS
# =====================================================

matches = (
    slack_df.join(
        sessions,
        on="user_id",
        how="inner"
    )
    .filter(
        (pl.col("slack_timestamp") >= pl.col("session_start"))
        & (pl.col("slack_timestamp") <= pl.col("session_end"))
    )
)

print("\n========== MATCHED SLACK MESSAGES ==========")
print(matches)


# =====================================================
# 6. COUNT POTENTIAL INTERRUPTIONS
# =====================================================

interruption_counts = (
    matches.group_by(["user_id", "session_id"])
    .agg(
        pl.len().alias("potential_slack_interruptions")
    )
)

sessions = sessions.join(
    interruption_counts,
    on=["user_id", "session_id"],
    how="left"
)

sessions = sessions.with_columns(
    pl.col("potential_slack_interruptions")
    .fill_null(0)
    .cast(pl.Int64)
)

sessions = sessions.with_columns(
    (
        (pl.col("duration_minutes") >= 90)
        & (pl.col("potential_slack_interruptions") == 0)
    ).alias("meets_90min_flow_criteria")
)

print("\n========== FINAL SESSION ANALYSIS ==========")
print(sessions)


# =====================================================
# 7. CONNECT TO MYSQL
# =====================================================

print("\n========== MYSQL CONNECTION ==========")

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="gitika_14",
    database="cognistream"
)

cursor = connection.cursor()

print("MySQL connection successful!")


# =====================================================
# 8. INSERT CODING SESSIONS INTO MYSQL
# =====================================================

session_id_mapping = {}

for row in sessions.to_dicts():

    query = """
    INSERT INTO coding_sessions
    (
        developer_id,
        session_start,
        session_end,
        total_events,
        duration_minutes,
        potential_slack_interruptions,
        meets_90min_flow_criteria
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    values = (
        str(row["user_id"]),
        row["session_start"],
        row["session_end"],
        row["total_events"],
        row["duration_minutes"],
        row["potential_slack_interruptions"],
        row["meets_90min_flow_criteria"]
    )

    cursor.execute(query, values)

    session_id_mapping[
        (row["user_id"], row["session_id"])
    ] = cursor.lastrowid


# =====================================================
# 9. INSERT MATCHED SLACK MESSAGES INTO MYSQL
# =====================================================

for row in matches.to_dicts():

    database_session_id = session_id_mapping[
        (row["user_id"], row["session_id"])
    ]

    query = """
    INSERT INTO session_interruptions
    (
        session_id,
        slack_timestamp,
        slack_message
    )
    VALUES (%s, %s, %s)
    """

    values = (
        database_session_id,
        row["slack_timestamp"],
        row["message"]
    )

    cursor.execute(query, values)


connection.commit()

print("\nCoding sessions and Slack matches inserted successfully!")


# =====================================================
# 10. SQL VALIDATION
# =====================================================

print("\n========== MYSQL VALIDATION ==========")

cursor.execute("""
SELECT
    session_id,
    developer_id,
    total_events,
    duration_minutes,
    potential_slack_interruptions,
    meets_90min_flow_criteria
FROM coding_sessions
""")

for row in cursor.fetchall():
    print(row)


cursor.execute("""
SELECT COUNT(*)
FROM session_interruptions
""")

print("\nTotal stored Slack interruptions:", cursor.fetchone()[0])


# =====================================================
# 11. CLOSE CONNECTION
# =====================================================

cursor.close()
connection.close()

print("\nMySQL connection closed.")

print("\n========== PIPELINE COMPLETED SUCCESSFULLY ==========")