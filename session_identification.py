import polars as pl
from datetime import datetime

# Synthetic IDE activity for testing
df = pl.DataFrame({
    "user_id": [1, 1, 1, 1, 1, 1],
    "event_timestamp": [
        datetime(2026, 10, 27, 10, 0),
        datetime(2026, 10, 27, 10, 5),
        datetime(2026, 10, 27, 10, 12),
        datetime(2026, 10, 27, 10, 50),
        datetime(2026, 10, 27, 10, 55),
        datetime(2026, 10, 27, 11, 30),
    ],
})

# Sort events chronologically for each user
df = df.sort(["user_id", "event_timestamp"])

# Calculate time gap between consecutive events
df = df.with_columns(
    pl.col("event_timestamp")
    .diff()
    .over("user_id")
    .alias("time_gap")
)

# Start a new session if the gap is greater than 15 minutes
df = df.with_columns(
    (
        pl.col("time_gap").is_null()
        | (pl.col("time_gap") > pl.duration(minutes=15))
    )
    .cast(pl.Int64)
    .alias("new_session")
)

# Assign session IDs
df = df.with_columns(
    pl.col("new_session")
    .cum_sum()
    .over("user_id")
    .alias("session_id")
)

print("\n=== IDE Activity with Session IDs ===")
print(df)

# Summarize each coding session
sessions = df.group_by(["user_id", "session_id"]).agg([
    pl.col("event_timestamp").min().alias("session_start"),
    pl.col("event_timestamp").max().alias("last_activity"),
    pl.len().alias("total_events"),
]).sort(["user_id", "session_id"])

sessions = sessions.with_columns(
    (
        pl.col("last_activity") - pl.col("session_start")
    ).alias("observed_span")
)

print("\n=== Identified Coding Sessions ===")
print(sessions)
