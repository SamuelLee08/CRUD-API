from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from db import get_db_connection

app = FastAPI()

class TaskCreate(BaseModel):
    title: str

class TaskUpdate(BaseModel):
    title: str
    done: bool | None = None


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
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM tasks")
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row is None:
        return JSONResponse(status_code=404, content={"error": "Task not found"})
    
    return dict(row)

@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate):
    title = task.title.strip()
    if not title:
        return JSONResponse(status_code=400, content={"error": "Title cannot be empty"})
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO tasks (title, done) VALUES (%s, %s) RETURNING id", (title, False))
    result = cursor.fetchone()
    new_id = result['id']
    conn.commit()
    conn.close()
    
    return {"id": new_id, "title": title, "done": False}

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: TaskUpdate):
    title = task.title.strip()
    if not title:
        return JSONResponse(status_code=400, content={"error": "Title cannot be empty"})
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
    existing = cursor.fetchone()
    
    if existing is None:
        conn.close()
        return JSONResponse(status_code=404, content={"error": "Task not found"})
    
    if task.done is not None:
        cursor.execute("UPDATE tasks SET title = %s, done = %s WHERE id = %s", 
                      (title, task.done, task_id))
    else:
        cursor.execute("UPDATE tasks SET title = %s WHERE id = %s", 
                      (title, task_id))
    
    conn.commit()
    conn.close()
    
    done_value = task.done if task.done is not None else existing["done"]
    return {"id": task_id, "title": title, "done": done_value}

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM tasks WHERE id = %s", (task_id,))
    if cursor.fetchone() is None:
        conn.close()
        return JSONResponse(status_code=404, content={"error": "Task not found"})
    
    cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
    conn.commit()
    conn.close()
    
    return None

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000)