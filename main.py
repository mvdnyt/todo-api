from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel


app=FastAPI()

tasks = [
    {"id": 1, "title": "Buy milk", "done": False},
    {"id": 2, "title": "Feed the cat", "done": True},
    {"id": 3, "title": "Write code", "done": False}

]

@app.get("/")
def root():
    "Tells you about the Main API"
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }
@app.get("/health")
def health():
    "Checks if the server is currently running"
    return {"status": "ok"}

@app.get("/tasks")
def get_tasks():
    "Return all tasks "
    return tasks

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    "Return a single task by id or return 404 error if it doesn't exist"
    for task in tasks:
        if task["id"] == task_id:
            return task
        
    raise HTTPException(status_code=404, detail= f"Task {task_id} not found")

class TaskCreate(BaseModel):
    title: str = ""
          
@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate):
    "Create a new task from title and add it to the list"
    if task.title.strip() == "":
        raise HTTPException(status_code=400, detail="title is required")
    ids = [t["id"] for t in tasks]
    new_id = max(ids) + 1
    new_task = {"id":new_id,"title":task.title,"done":False}
    tasks.append(new_task)
    return (new_task)

class TaskUpdate(BaseModel):
    title: str | None=None
    done: bool | None=None 

@app.put("/tasks/{task_id}")
def put_task(task_id:int, task: TaskUpdate):
    "Update a tasks title and/or done status"
    if task.title is not None and task.title.strip() == "":
        raise HTTPException(status_code=400, detail="title is required")
    for t in tasks:
       if t["id"]==task_id: 
        if task.title is not None:
            t["title"] = task.title
        if task.done is not None:
            t["done"] = task.done
        return t    
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id:int ):
    "Delete a task by id"
    for t in tasks:
        if t["id"] == task_id:
            tasks.remove(t)
            return None
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")       
