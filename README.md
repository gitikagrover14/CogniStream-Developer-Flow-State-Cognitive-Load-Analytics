# CogniStream: Developer Flow-State & Cognitive Load Analytics

## Problem Statement

Engineering productivity is often measured using flawed metrics like "lines of code written" or "tickets closed." These ignore the friction of the development process and fail to identify what blocks deep, focused work.

CogniStream addresses this by analyzing developer flow state and cognitive load, highlighting interruptions such as poorly timed CI/CD alerts that reduce productivity.

## Use Case

An Engineering Manager can review the CogniStream dashboard to see a "Context-Switching Tax" analysis. Data shows how much focus time is lost due to interruptions, enabling managers to adjust notification policies and improve developer experience.

## Key Modules

* **Orchestration (Apache Airflow):** Scheduled DAGs pulling event logs from developer APIs (GitHub, Jira, Slack, VSCode Activity Watch).
* **OLAP Database (ClickHouse):** Optimized for ingesting and querying massive volumes of timestamped event logs.
* **Data Processing (Python & Polars):** High-speed data manipulation to calculate continuous "Flow State" blocks and identify interruption triggers.
* **Custom Dashboard (React & Tremor.js):** Developer-centric frontend with analytics components.

## Dashboard Features

* Reusable metric cards for displaying productivity metrics.
* Activity summary cards for GitHub, Slack, and IDE activity.
* Mock activity events to demonstrate dashboard functionality.
* Activity filtering by source: All, GitHub, Slack, and IDE.
* Empty-state handling when no activity events are available.
* Responsive dashboard layout.

## Technology Stack

* React
* Vite
* JavaScript
* CSS
* Mock data for frontend development

## Week 2 Development & Testing

The Week 2 frontend work focuses on developing the dashboard using mock data.

### Completed Work

* Organized metric and activity data into separate data files.
* Added reusable dashboard components.
* Implemented activity filtering.
* Added an empty-state message for scenarios with no activity events.
* Added a new mock GitHub commit event for testing.

### Testing Results

The dashboard was tested with different mock-data scenarios.

| Test Scenario        | Expected Result                            | Status |
| -------------------- | ------------------------------------------ | ------ |
| All activity sources | 7 events displayed                         | Passed |
| GitHub filter        | 3 events displayed                         | Passed |
| Slack filter         | 2 events displayed                         | Passed |
| IDE filter           | 2 events displayed                         | Passed |
| Empty activity data  | Empty-state message displayed              | Passed |
| New mock event       | Dashboard updates to display the new event | Passed |

*Note: These results are based on local frontend testing with mock data. They do not indicate that live GitHub, Slack, or IDE integrations are connected.*

## Development Plan

* **Week 1:** API ingestion (GitHub, Slack, IDE) + Airflow scheduling; UI scaffolding with React & Tremor.js.
* **Week 2:** Data modeling in ClickHouse; base metrics in UI. Frontend dashboard development and mock-data testing are in progress/completed for the tasks described above.
* **Week 3:** Flow-state logic with SQL/Polars; friction UI charts.
* **Week 4:** API layer with FastAPI; dashboard refinement and polish.

## Outcome

* A planned orchestration engine merging diverse event logs into a unified OLAP schema.
* A specialized analytics UI measuring developer friction rather than just output.
* A frontend dashboard that can be tested with mock activity data.

## Contributors

* Gitika (Team Leader)
* Rahul (Team Member)
* Avadhut (Team Member)
