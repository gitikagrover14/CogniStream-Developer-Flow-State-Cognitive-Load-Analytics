import polars as pl
from datetime import datetime

# =====================================================
# 1. SAMPLE IDE ACTIVITY DATA
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
    ],
})

# Sort events chronologically
ide_df = ide_df.sort(["user_id", "event_timestamp"])

# =====================================================
# 2. IDENTIFY CODING SESSIONS
# =====================================================

ide_df = ide_df.with_columns(
    pl.col("event_timestamp")
    .diff()
    .over("user_id")
    .alias("time_gap")
)

# A new session begins when inactivity exceeds 15 minutes
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

# Summarize each session
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
    ).alias("observed_span")
)

print("\n========== CODING SESSIONS ==========")
print(sessions)

# =====================================================
# 3. SAMPLE SLACK MESSAGE DATA
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
    ],
})

# =====================================================
# 4. MATCH SLACK MESSAGES WITH CODING SESSIONS
# =====================================================

matches = (
    slack_df.join(
        sessions,
        on="user_id",
        how="inner",
    )
    .filter(
        (pl.col("slack_timestamp") >= pl.col("session_start"))
        & (pl.col("slack_timestamp") <= pl.col("session_end"))
    )
    .sort(["user_id", "slack_timestamp"])
)

print("\n========== SLACK MESSAGES MATCHING SESSIONS ==========")

if matches.height > 0:
    print(
        matches.select([
            "user_id",
            "session_id",
            "slack_timestamp",
            "message",
            "session_start",
            "session_end",
        ])
    )
else:
    print("No Slack messages matched with coding sessions.")

# =====================================================
# 5. COUNT POTENTIAL SLACK INTERRUPTIONS
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
    how="left",
)

sessions = sessions.with_columns(
    pl.col("potential_slack_interruptions")
    .fill_null(0)
    .cast(pl.Int64)
)

# =====================================================
# 6. CHECK THE 90-MINUTE FLOW CRITERION
# =====================================================

sessions = sessions.with_columns(
    (
        (pl.col("observed_span") >= pl.duration(minutes=90))
        & (pl.col("potential_slack_interruptions") == 0)
    ).alias("meets_90min_uninterrupted_flow_criteria")
)

print("\n========== 90-MINUTE FLOW ANALYSIS ==========")

print(
    sessions.select([
        "user_id",
        "session_id",
        "session_start",
        "session_end",
        "total_events",
        "observed_span",
        "potential_slack_interruptions",
        "meets_90min_uninterrupted_flow_criteria",
    ])
)

# =====================================================
# 7. FINAL SUMMARY
# =====================================================

total_sessions = sessions.height

sessions_over_90 = sessions.filter(
    pl.col("observed_span") >= pl.duration(minutes=90)
).height

sessions_meeting_criteria = sessions.filter(
    pl.col("meets_90min_uninterrupted_flow_criteria")
).height

total_potential_interruptions = (
    sessions.get_column("potential_slack_interruptions").sum()
)

print("\n========== FINAL SUMMARY ==========")
print(f"Total coding sessions: {total_sessions}")
print(f"Sessions with observed span >= 90 minutes: {sessions_over_90}")
print(f"Sessions meeting the 90-minute flow criteria: {sessions_meeting_criteria}")
print(f"Potential Slack interruptions matched: {total_potential_interruptions}")

print("\nNote: This analysis uses synthetic sample data.")
print("A matched Slack message indicates a potential interruption,")
print("not proof that coding was actually interrupted.")
print("Observed event span does not prove continuous coding time.")