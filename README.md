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

### URL Monitoring

* Add URLs
* Delete URLs
* Refresh all URLs
* Check status (UP / DOWN)
* Response time tracking

### Database

Tables used:

* users
* urls
* check_results

### Logging

System logs URL check results in terminal.

Example:
Checked URL: https://google.com, Status: UP, Response: 1368ms

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

Open frontend folder using Live Server

---

## Sample Login Credentials

Example:

username: demo
password: 123

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

## Design Decisions and Tradeoffs

* FastAPI chosen for simplicity and speed
* MySQL chosen for relational structure
* Frontend kept lightweight for quick interaction
* JWT was not fully implemented to keep focus on core monitoring logic

---

## AI Usage

AI assistance was used for:

* Debugging errors
* Structuring backend layers
* Improving frontend interactions
* Refining project architecture

Final integration, testing, and debugging were manually completed.
