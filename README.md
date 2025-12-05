# IT Automation & Incident Response System (ITAIRS)

A professional-grade **IT Automation & Incident Response Platform** designed to simulate real enterprise help desk and sysadmin workflows.

This project combines **FastAPI**, **Python automation scripts**, **PowerShell collectors**, and a lightweight **incident timeline dashboard** to demonstrate:

- IT engineering foundations
- backend/API development
- automated diagnostics
- event tracking
- log analysis
- system-level troubleshooting processes

## Features

- `/api/health` – simple health check
- `/api/system/info` – system hostname, OS, uptime, CPU, memory, and disk usage
- `/api/network/ping` – basic ping diagnostic endpoint
- `/api/incidents` – create & list incidents with severity, source, and category
- `/api/events` – create & list event logs
- Python automation scripts for diagnostics & log parsing
- PowerShell scripts for Windows event log collection and basic remediation
- Simple HTML/CSS/JS dashboard to visualize system info, incidents, and events

## Run locally

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

### Frontend

```bash
cd frontend
# Serve index.html or open directly in a browser
```

## Docker

From project root:

```bash
docker-compose up --build
```

This starts:

- `backend` on `http://localhost:8000`
- `frontend` dashboard on `http://localhost:8081`
