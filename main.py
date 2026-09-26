from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, field_validator

app = FastAPI()

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

@app.post("/tasks", status_code=201)
def create_task(task_data: TaskCreate):
    new_id = max(task.id for task in tasks) + 1

    new_task = Task(
        id=new_id,
        title=task_data.title,
        done=False
    )

    tasks.append(new_task)

    return new_task