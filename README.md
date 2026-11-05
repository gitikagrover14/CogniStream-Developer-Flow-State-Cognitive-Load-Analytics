# CogniStream Backend API

## Project Overview

CogniStream is a Developer Flow-State and Cognitive Load Analytics project designed to analyse coding sessions, Slack interruptions, and developer productivity patterns.

This backend is being developed using FastAPI and MySQL to provide structured data to the React dashboard.

## Technologies Used

* Python
* FastAPI
* Uvicorn
* MySQL
* Polars

## Backend Structure

```text
backend/
├── main.py
├── requirements.txt
└── README.md
```

## API Endpoints

| Method | Endpoint           | Description                  |
| ------ | ------------------ | ---------------------------- |
| GET    | /                  | Backend welcome message      |
| GET    | /api/health        | Check backend status         |
| GET    | /api/summary       | Dashboard summary metrics    |
| GET    | /api/sessions      | Retrieve coding sessions     |
| GET    | /api/interruptions | Retrieve Slack interruptions |

## Setup Instructions

Install the required dependencies:

```bash
python -m pip install -r backend/requirements.txt
```

## Run the Backend

```bash
python -m uvicorn backend.main:app --reload
```

## API Documentation

Once the backend is running, access the interactive API documentation at:

http://127.0.0.1:8000/docs

## Current Status

Initial FastAPI application and API endpoint structure have been created.

MySQL connectivity, actual database queries, and frontend integration will be implemented in subsequent development stages.
