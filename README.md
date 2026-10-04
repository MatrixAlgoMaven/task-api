# Task API

A simple CRUD Task API built with Python, FastAPI, and SQLite.

The API stores tasks in a SQLite database and supports creating, reading, updating, and deleting tasks. Data persists even when the server is restarted.

## Features

- Create tasks
- List all tasks
- Get a task by ID
- Update a task
- Delete a task
- SQLite database storage
- Automatic database and table creation
- Three example tasks created when the database is empty
- Data persistence across server restarts
- Validation for missing or empty titles
- Proper HTTP status codes
- Interactive Swagger UI documentation

## Requirements

- Python 3.10+
- FastAPI
- Uvicorn
- SQLite

SQLite is included with Python, so no separate database installation is required.

## Installation and Setup

Clone the repository:

```bash
git clone https://github.com/MatrixAlgoMaven/task-api.git
cd task-api