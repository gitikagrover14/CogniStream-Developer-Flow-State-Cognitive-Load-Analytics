from fastapi import FastAPI

app = FastAPI(
    title="CogniStream API",
    description="Backend API for Developer Flow-State and Cognitive Load Analytics",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "project": "CogniStream",
        "message": "CogniStream API is running successfully!",
        "status": "success"
    }


@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "message": "Backend is working properly"
    }


@app.get("/api/summary")
def dashboard_summary():
    return {
        "total_sessions": 0,
        "total_interruptions": 0,
        "average_session_duration": 0,
        "flow_sessions": 0
    }


@app.get("/api/sessions")
def get_sessions():
    return {
        "message": "Coding sessions endpoint",
        "data": []
    }


@app.get("/api/interruptions")
def get_interruptions():
    return {
        "message": "Slack interruptions endpoint",
        "data": []
    }
