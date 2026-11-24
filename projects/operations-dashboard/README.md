# Operations Dashboard

A web application that converts validated network-audit results into accountable work: triage, assignment, remediation tracking, independent verification, historical reporting, and optical-signal monitoring.

## Architecture

- Flask application with server-rendered views and a small static frontend.
- SQLite operational store separated from read-only audit history.
- Argon2 password hashing, CSRF controls, rate limits, revocable sessions, and role-based authorization.
- Source adapters reject incomplete, inconsistent, partial, or future-dated audit runs.

## Run locally

From the repository root:

```powershell
.\scripts\setup.ps1
.\.venv\Scripts\python.exe .\projects\operations-dashboard\demo\app.py
```

Open `http://127.0.0.1:5000`. The JSON endpoint is available at `/api/cases`.
Linux and macOS users can replace `.\.venv\Scripts\python.exe` with `.venv/bin/python`.

The demo uses three synthetic cases. The public edition intentionally excludes production databases, admin accounts, session keys, exports, and LAN configuration.

## Portfolio value

This project demonstrates full-stack Python development, security-conscious authentication, data validation, operational UX, reporting, and test-driven evolution of a business workflow.

