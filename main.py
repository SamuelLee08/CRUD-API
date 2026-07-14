from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI()

class TaskCreate(BaseModel):
    title: str
class TaskUpdate(BaseModel):
    title: str
    done: bool | None = None

tasks = [
    {"id": 1, "title": "Buy milk", "done": False},
    {"id": 2, "title": "Walk the dog", "done": True},
    {"id": 3, "title": "Study FastAPI", "done": False},
]

@app.get("/")
def root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/tasks")
def list_tasks():
    return tasks

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    return JSONResponse(status_code=404, content={"error": f"Task {task_id} not found"})

@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate):
    title = task.title.strip()
    if not title:
        return JSONResponse(status_code=400, content={"error": "Title cannot be empty"})
    new_id = max((t["id"] for t in tasks), default=0) + 1
    new_task = {"id": new_id, "title": title, "done": False}
    tasks.append(new_task)
    return new_task

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: TaskUpdate):
    for existing in tasks:
        if existing["id"] == task_id:
            title = task.title.strip()
            if not title:
                return JSONResponse(status_code=400, content={"error": "Title cannot be empty"})
            existing["title"] = title
            if task.done is not None:
                existing["done"] = task.done
            return existing
    return JSONResponse(status_code=404, content={"error": f"Task {task_id} not found"})

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    for existing in tasks:
        if existing["id"] == task_id:
            tasks.remove(existing)
            return
    return JSONResponse(status_code=404, content={"error": f"Task {task_id} not found"})