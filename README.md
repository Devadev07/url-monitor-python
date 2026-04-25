# URL Health & Observability Platform

## Overview

This project is a full-stack URL monitoring platform built using FastAPI, MySQL, and a frontend with HTML, CSS, and JavaScript.

It allows users to:

* Sign up and log in securely
* Add and manage monitored URLs
* Check URL health status
* Measure response time
* View monitoring results in dashboard form

---

## Features

### Authentication

* User signup
* User login
* Password hashing using bcrypt
* JWT token generation with expiry
* Protected routes using Bearer token

### URL Monitoring

* Add URLs
* Delete URLs
* Check single URL
* Refresh all URLs
* Check status (UP / DOWN)
* Response time tracking
* Failure reason tracking

### Database

Tables used:

* users
* urls
* check_results

### Logging

System logs URL checks using Python logging with INFO, WARNING, and ERROR levels.

Example:

2026-04-25 00:10:11 - INFO - URL checked successfully (google.com) - 1368ms

---

## Project Structure

app/

* core/
* models/
* repositories/
* routes/
* schemas/
* services/

frontend/

* login.html
* dashboard.html
* auth.js
* url.js
* style.css

---

## Setup Instructions

### 1. Create virtual environment

python -m venv venv

### 2. Activate environment

Windows:

venv\Scripts\activate

### 3. Install dependencies

pip install -r requirements.txt

### 4. Configure environment

Create `.env` using `.env.example`

### 5. Run backend

python -m uvicorn app.main:app --reload

### 6. Run frontend

python -m http.server 5500

---

## Sample Login Credentials

Sample credentials can be created using signup from the frontend login page.

---

## Architecture Overview

Frontend communicates with FastAPI backend using REST APIs.

Backend layers:

* Routes
* Services
* Repository
* Models

Database stores user URLs and monitoring history.

---

## Design Notes

### Concurrency

URL checks were changed from sequential execution to concurrent async execution using asyncio.gather(), allowing multiple URLs to be checked at the same time. This prevents one slow or failed URL from blocking others. The tradeoff is that very large batches may require concurrency limits later to control resource usage.

### Scheduling

A background scheduler using APScheduler was added so checks run automatically at fixed intervals and restart when the server restarts. URL check intervals are stored per URL for future extensibility. The current tradeoff is that scheduling runs in periodic batches rather than fully separate per-URL jobs.

### Authentication

JWT authentication was implemented end to end using token generation during login, token expiry, and protected routes requiring Bearer tokens. This keeps authentication stateless and simple for frontend integration. The tradeoff is that token invalidation before expiry would require additional token revocation logic later.

### Error Handling

Explicit handling was added for invalid URLs, DNS failures, connection timeouts, and non-2xx HTTP responses. Failures are stored as DOWN status together with the reason in the database and shown in the dashboard. The tradeoff is that some lower-level network exceptions are grouped into broader categories for readability.

### Logging

Python logging replaced print statements, using INFO for successful checks, WARNING for DOWN results, and ERROR for exceptions. Logs include timestamps and context for each monitored URL. The tradeoff is that log rotation is not yet configured for long-running deployments.

---

## AI Usage

AI assistance was used for:

* Debugging errors
* Structuring backend layers
* Improving frontend interactions
* Refining project architecture

Final integration, testing, and debugging were manually completed.
