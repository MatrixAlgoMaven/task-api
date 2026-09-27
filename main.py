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

class TaskUpdate(BaseModel):
    title: str | None = None
    done: bool | None = None

tasks = [
    Task(id=1, title="Learn FastAPI", done=False),
    Task(id=2, title="Build Task API", done=False),
    Task(id=3, title="Practice Python", done=True),
]

@app.get("/", summary="Check that the API is running")
def root():
    return {"message": "Hello, Task API!"}


@app.get("/tasks", summary="List all tasks")
def get_tasks():
    return tasks


@app.get("/tasks/{id}", summary="Get a task by ID")
def get_task(id: int):
    for task in tasks:
        if task.id == id:
            return task

    return JSONResponse(
        status_code=404,
        content={"error": f"Task {id} not found"}
    )

@app.put("/tasks/{id}", summary="Update a task")
def update_task(id: int, task_data: TaskUpdate):
    for task in tasks:
        if task.id == id:

            if task_data.title is not None:
                if not task_data.title.strip():
                    return JSONResponse(
                        status_code=400,
                        content={"error": "Title cannot be empty"}
                    )
                task.title = task_data.title

            if task_data.done is not None:
                task.done = task_data.done

            return task

    return JSONResponse(
        status_code=404,
        content={"error": f"Task {id} not found"}
    )

@app.delete("/tasks/{id}", status_code=204, summary="Delete a task")
def delete_task(id: int):
    for task in tasks:
        if task.id == id:
            tasks.remove(task)
            return

    return JSONResponse(
        status_code=404,
        content={"error": f"Task {id} not found"}
    )

@app.post("/tasks", status_code=201, summary="Create a new task")
def create_task(task_data: TaskCreate):
    new_id = max(task.id for task in tasks) + 1

    new_task = Task(
        id=new_id,
        title=task_data.title,
        done=False
    )

    tasks.append(new_task)

    return new_task
