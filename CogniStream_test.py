import unittest
from datetime import datetime, timedelta
import polars as pl


# ==========================================
# 1. CONFIGURATION
# ==========================================

SESSION_GAP = 15
FLOW_DURATION = 90


# ==========================================
# 2. SESSION IDENTIFICATION FUNCTION
# ==========================================

def identify_sessions(ide_df):

    if ide_df.is_empty():
        raise ValueError("IDE dataset is empty.")

    if ide_df["event_timestamp"].null_count() > 0:
        raise ValueError("IDE timestamps contain null values.")

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
            | (pl.col("time_gap") > pl.duration(minutes=SESSION_GAP))
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
            pl.len().alias("total_events")
        ])
        .sort(["user_id", "session_id"])
    )

    sessions = sessions.with_columns(
        (
            pl.col("session_end") - pl.col("session_start")
        ).dt.total_minutes().alias("duration_minutes")
    )

    return sessions


# ==========================================
# 3. SLACK MATCHING FUNCTION
# ==========================================

def match_slack_messages(slack_df, sessions):

    if slack_df["slack_timestamp"].null_count() > 0:
        raise ValueError("Slack timestamps contain null values.")

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
        .sort(["user_id", "slack_timestamp"])
    )

    return matches


# ==========================================
# 4. FLOW CRITERIA FUNCTION
# ==========================================

def check_flow_criteria(sessions, matches):

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
            (pl.col("duration_minutes") >= FLOW_DURATION)
            & (pl.col("potential_slack_interruptions") == 0)
        ).alias("meets_90min_flow_criteria")
    )

    return sessions


# ==========================================
# 5. TEST DATA HELPER FUNCTIONS
# ==========================================

def make_time(hour, minute=0):

    return datetime(2026, 10, 27, hour, minute)


def create_ide_session(start_hour, start_minute, duration):

    start = make_time(start_hour, start_minute)

    timestamps = [
        start + timedelta(minutes=i)
        for i in range(0, duration + 1, 10)
    ]

    if timestamps[-1] != start + timedelta(minutes=duration):
        timestamps.append(
            start + timedelta(minutes=duration)
        )

    return pl.DataFrame({
        "user_id": [1] * len(timestamps),
        "event_timestamp": timestamps
    })


def create_empty_slack():

    return pl.DataFrame({
        "user_id": pl.Series([], dtype=pl.Int64),
        "slack_timestamp": pl.Series([], dtype=pl.Datetime),
        "message": pl.Series([], dtype=pl.String)
    })


# ==========================================
# 6. AUTOMATED TEST CASES
# ==========================================

class TestCogniStream(unittest.TestCase):

    # Test 1: Session identification

    def test_01_session_identification(self):

        ide = pl.DataFrame({
            "user_id": [1, 1, 1, 1],
            "event_timestamp": [
                make_time(9, 0),
                make_time(9, 10),
                make_time(9, 20),
                make_time(10, 0)
            ]
        })

        sessions = identify_sessions(ide)

        self.assertEqual(sessions.height, 2)


    # Test 2: Exactly 15-minute gap

    def test_02_exactly_15_min_gap(self):

        ide = pl.DataFrame({
            "user_id": [1, 1],
            "event_timestamp": [
                make_time(9, 0),
                make_time(9, 15)
            ]
        })

        sessions = identify_sessions(ide)

        self.assertEqual(sessions.height, 1)


    # Test 3: Single IDE event

    def test_03_single_event(self):

        ide = pl.DataFrame({
            "user_id": [1],
            "event_timestamp": [make_time(9, 0)]
        })

        sessions = identify_sessions(ide)

        self.assertEqual(sessions.height, 1)

        self.assertEqual(
            sessions.item(0, "duration_minutes"), 0
        )


    # Test 4: Multiple users

    def test_04_multiple_users(self):

        ide = pl.DataFrame({
            "user_id": [1, 2, 1, 2],
            "event_timestamp": [
                make_time(9, 0),
                make_time(9, 0),
                make_time(9, 10),
                make_time(9, 10)
            ]
        })

        sessions = identify_sessions(ide)

        self.assertEqual(sessions.height, 2)


    # Test 5: Slack message matching

    def test_05_slack_matching(self):

        ide = create_ide_session(9, 0, 100)

        sessions = identify_sessions(ide)

        slack = pl.DataFrame({
            "user_id": [1, 1, 1],
            "slack_timestamp": [
                make_time(8, 50),
                make_time(9, 30),
                make_time(11, 0)
            ],
            "message": [
                "Before session",
                "Inside session",
                "After session"
            ]
        })

        matches = match_slack_messages(slack, sessions)

        self.assertEqual(matches.height, 1)


    # Test 6: Multiple Slack messages

    def test_06_multiple_slack_messages(self):

        ide = create_ide_session(9, 0, 100)

        sessions = identify_sessions(ide)

        slack = pl.DataFrame({
            "user_id": [1, 1],
            "slack_timestamp": [
                make_time(9, 20),
                make_time(9, 50)
            ],
            "message": [
                "Team update",
                "Notification"
            ]
        })

        matches = match_slack_messages(slack, sessions)

        result = check_flow_criteria(sessions, matches)

        self.assertEqual(
            result.item(0, "potential_slack_interruptions"), 2
        )


    # Test 7: 90-minute uninterrupted flow

    def test_07_ninety_minute_flow(self):

        ide = create_ide_session(9, 0, 90)

        sessions = identify_sessions(ide)

        slack = create_empty_slack()

        matches = match_slack_messages(slack, sessions)

        result = check_flow_criteria(sessions, matches)

        self.assertTrue(
            result.item(0, "meets_90min_flow_criteria")
        )


    # Test 8: Slack interruption during session

    def test_08_interruption_prevents_flow(self):

        ide = create_ide_session(9, 0, 100)

        sessions = identify_sessions(ide)

        slack = pl.DataFrame({
            "user_id": [1],
            "slack_timestamp": [make_time(9, 30)],
            "message": ["Team notification"]
        })

        matches = match_slack_messages(slack, sessions)

        result = check_flow_criteria(sessions, matches)

        self.assertFalse(
            result.item(0, "meets_90min_flow_criteria")
        )


    # Test 9: Less than 90-minute session

    def test_09_less_than_90_minutes(self):

        ide = create_ide_session(9, 0, 89)

        sessions = identify_sessions(ide)

        slack = create_empty_slack()

        matches = match_slack_messages(slack, sessions)

        result = check_flow_criteria(sessions, matches)

        self.assertFalse(
            result.item(0, "meets_90min_flow_criteria")
        )


# ==========================================
# 7. RUN ALL TESTS
# ==========================================

if __name__ == "__main__":

    print("\n====================================")
    print(" COGNISTREAM AUTOMATED TESTING")
    print("====================================\n")

    unittest.main(verbosity=2)
