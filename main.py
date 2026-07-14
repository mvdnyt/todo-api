from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel


app=FastAPI()

tasks = [
    {"id": 1, "title": "Buy milk", "done": False},
    {"id": 2, "title": "Feed the car", "done": True},
    {"id": 3, "title": "Write code", "done": False}

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
def get_tasks():
    return tasks

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
        
    raise HTTPException(status_code=404, detail= f"Task {task_id} not found")

class TaskCreate(BaseModel):
    title: str = ""
          
@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate):
    if task.title.strip() == "":
        raise HTTPException(status_code=400, detail="title is required")
    ids = [t["id"] for t in tasks]
    new_id = max(ids) + 1
    new_task = {"id":new_id,"title":task.title,"done":False}
    tasks.append(new_task)
    return (new_task)
   
