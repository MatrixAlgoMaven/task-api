from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI()


class Task(BaseModel):
    id: int
    title: str
    done: bool


tasks = [
    Task(id=1, title="Learn FastAPI", done=False),
    Task(id=2, title="Build Task API", done=False),
    Task(id=3, title="Practice Python", done=True),
]


@app.get("/")
def root():
    return {"message": "Hello, Task API!"}


@app.get("/tasks")
def get_tasks():
    return tasks


@app.get("/tasks/{id}")
def get_task(id: int):
    for task in tasks:
        if task.id == id:
            return task

    return JSONResponse(
        status_code=404,
        content={"error": f"Task {id} not found"}
    )