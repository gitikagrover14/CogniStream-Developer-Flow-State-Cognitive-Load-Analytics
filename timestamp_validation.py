
import pandas as pd

# Sample IDE events for testing session detection
ide_events = pd.DataFrame([
    {"user_id": 1, "event": "coding", "timestamp": "2026-10-27 10:00:00"},
    {"user_id": 1, "event": "coding", "timestamp": "2026-10-27 10:05:00"},
    {"user_id": 1, "event": "coding", "timestamp": "2026-10-27 10:12:00"},
    {"user_id": 1, "event": "coding", "timestamp": "2026-10-27 10:50:00"},
    {"user_id": 1, "event": "coding", "timestamp": "2026-10-27 10:55:00"},
])

# Sample Slack messages for testing interruption detection
slack_events = pd.DataFrame([
    {"user_id": 1, "message": "Build failed", "timestamp": "2026-10-27 10:08:00"},
    {"user_id": 1, "message": "Team update", "timestamp": "2026-10-27 10:30:00"},
    {"user_id": 1, "message": "Review request", "timestamp": "2026-10-27 10:52:00"},
])

# Convert timestamps to datetime
ide_events["timestamp"] = pd.to_datetime(ide_events["timestamp"])
slack_events["timestamp"] = pd.to_datetime(slack_events["timestamp"])

# Sort IDE events
ide_events = ide_events.sort_values(["user_id", "timestamp"])

# Start a new session when the gap exceeds 15 minutes
ide_events["gap_minutes"] = (
    ide_events.groupby("user_id")["timestamp"]
    .diff()
    .dt.total_seconds()
    .div(60)
)

ide_events["new_session"] = (
    ide_events["gap_minutes"].isna()
    | (ide_events["gap_minutes"] > 15)
)

ide_events["session_id"] = (
    ide_events.groupby("user_id")["new_session"].cumsum()
)

print("\n=== IDE SESSION DETECTION ===")
print(ide_events.to_string(index=False))

# Calculate session start, end, and observed duration
sessions = (
    ide_events.groupby(["user_id", "session_id"])
    .agg(
        session_start=("timestamp", "min"),
        last_observed_event=("timestamp", "max"),
        event_count=("timestamp", "count"),
    )
    .reset_index()
)

sessions["observed_span_minutes"] = (
    sessions["last_observed_event"] - sessions["session_start"]
).dt.total_seconds() / 60

print("\n=== CODING SESSIONS ===")
print(sessions.to_string(index=False))

# Identify Slack messages occurring within session intervals
print("\n=== POTENTIAL SLACK INTERRUPTIONS ===")

for _, session in sessions.iterrows():
    matching_messages = slack_events[
        (slack_events["user_id"] == session["user_id"])
        & (slack_events["timestamp"] >= session["session_start"])
        & (slack_events["timestamp"] <= session["last_observed_event"])
    ]

    print(
        f"\nSession {session['session_id']}: "
        f"{session['session_start']} to "
        f"{session['last_observed_event']}"
    )

    if matching_messages.empty:
        print("No Slack messages observed within this session.")
    else:
        print(matching_messages.to_string(index=False))

print("\nNote: These are synthetic sample events, not real user activity.")
