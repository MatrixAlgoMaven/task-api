from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, field_validator
import sqlite3

app = FastAPI()


# -----------------------------
# Database setup
# -----------------------------

def get_connection():
    return sqlite3.connect("tasks.db")


def initialize_database():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            done BOOLEAN NOT NULL
        )
    """)

    cursor.execute("SELECT COUNT(*) FROM tasks")
    count = cursor.fetchone()[0]

    if count == 0:
        cursor.executemany(
            "INSERT INTO tasks (id, title, done) VALUES (?, ?, ?)",
            [
                (1, "Learn FastAPI", False),
                (2, "Build Task API", False),
                (3, "Practice Python", True),
            ]
        )

    connection.commit()
    connection.close()


initialize_database()


# -----------------------------
# Validation
# -----------------------------

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    return JSONResponse(
        status_code=400,
        content={"error": "Title is required"}
    )


class Task(BaseModel):
    id: int
    title: str
    done: bool


class TaskCreate(BaseModel):
    title: str

    @field_validator("title")
    @classmethod
    def title_must_not_be_empty(cls, value):
        if not value.strip():
            raise ValueError("Title cannot be empty")
        return value


class TaskUpdate(BaseModel):
    title: str | None = None
    done: bool | None = None


# -----------------------------
# API
# -----------------------------

@app.get("/", summary="Check that the API is running")
def root():
    return {"message": "Hello, Task API!"}


@app.get("/tasks", summary="List all tasks")
def get_tasks():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT id, title, done FROM tasks")
    rows = cursor.fetchall()

    connection.close()

    return [
        Task(id=row[0], title=row[1], done=bool(row[2]))
        for row in rows
    ]

@app.get("/tasks/{id}", summary="Get a task by ID")
def get_task(id: int):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT id, title, done FROM tasks WHERE id = ?",
        (id,)
    )

    row = cursor.fetchone()

    connection.close()

    if row is None:
        return JSONResponse(
            status_code=404,
            content={"error": f"Task {id} not found"}
        )

    return Task(
        id=row[0],
        title=row[1],
        done=bool(row[2])
    )