import mysql.connector
from fastapi import FastAPI, HTTPException

app = FastAPI(
    title="CogniStream API",
    description="Developer Flow-State and Cognitive Load Analytics",
    version="1.0.0"
)


# ==========================================
# MySQL Database Connection
# ==========================================

def get_connection():

    try:
        connection = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="****",
            password="****",
            database="cognistream"
        )

        return connection

    except mysql.connector.Error as error:
        raise HTTPException(
            status_code=500,
            detail=f"MySQL connection failed: {error}"
        )


# ==========================================
# Home Endpoint
# ==========================================

@app.get("/")
def home():

    return {
        "project": "CogniStream",
        "message": "CogniStream API is running successfully!",
        "status": "success"
    }


# ==========================================
# Database Health Check
# ==========================================

@app.get("/api/health")
def health_check():

    connection = get_connection()

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT DATABASE()")

        database_name = cursor.fetchone()[0]

        return {
            "status": "healthy",
            "database": database_name,
            "message": "MySQL connection successful"
        }

    finally:
        cursor.close()
        connection.close()


# ==========================================
# Dashboard Summary
# ==========================================

@app.get("/api/summary")
def dashboard_summary():

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            "SELECT COUNT(*) FROM coding_sessions"
        )
        total_sessions = cursor.fetchone()[0]

        cursor.execute(
            "SELECT COUNT(*) FROM session_interruptions"
        )
        total_interruptions = cursor.fetchone()[0]

        return {
            "total_sessions": total_sessions,
            "total_interruptions": total_interruptions
        }

    finally:
        cursor.close()
        connection.close()


# ==========================================
# Retrieve Coding Sessions
# ==========================================

@app.get("/api/sessions")
def get_sessions():

    connection = get_connection()

    try:
        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT * FROM coding_sessions")
        sessions = cursor.fetchall()

        return {
            "total_sessions": len(sessions),
            "data": sessions
        }

    finally:
        cursor.close()
        connection.close()


# ==========================================
# Retrieve Slack Interruptions
# ==========================================

@app.get("/api/interruptions")
def get_interruptions():

    connection = get_connection()

    try:
        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT * FROM session_interruptions")
        interruptions = cursor.fetchall()

        return {
            "total_interruptions": len(interruptions),
            "data": interruptions
        }

    finally:
        cursor.close()
        connection.close()

# ==========================================
# DAY 3 - API DEVELOPMENT
# ==========================================

# 1. Session Duration Metrics
@app.get("/api/metrics/duration")
def session_duration_metrics():

    connection = get_connection()

    try:
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                COUNT(*) AS total_sessions,
                AVG(duration_minutes) AS average_duration_minutes,
                MAX(duration_minutes) AS longest_session_minutes,
                MIN(duration_minutes) AS shortest_session_minutes
            FROM coding_sessions
        """)

        metrics = cursor.fetchone()

        return {
            "status": "success",
            "duration_metrics": metrics
        }

    finally:
        cursor.close()
        connection.close()


# 2. 90-Minute Uninterrupted Flow Metrics
@app.get("/api/metrics/flow")
def flow_metrics():

    connection = get_connection()

    try:
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                COUNT(*) AS total_sessions,
                SUM(meets_90min_flow_criteria) AS qualifying_sessions
            FROM coding_sessions
        """)

        metrics = cursor.fetchone()

        total_sessions = metrics["total_sessions"] or 0
        qualifying_sessions = metrics["qualifying_sessions"] or 0

        return {
            "status": "success",
            "flow_metrics": {
                "total_sessions": total_sessions,
                "qualifying_sessions": qualifying_sessions,
                "non_qualifying_sessions": (
                    total_sessions - qualifying_sessions
                ),
                "flow_criteria_minutes": 90
            }
        }

    finally:
        cursor.close()
        connection.close()
