from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.task import Task
from app.db.deps import get_db

router = APIRouter(prefix="/tasks")
 
# CRUD の実装を行う

## Create
@router.post("/")
def create_task(title: str, db: Session = Depends(get_db)):
    task = Task(title=title)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

## Read 一件取得
@router.get("/{task_id}")
def read_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    return task

## Read 一覧取得
@router.get("/")
def read_tasks(db: Session = Depends(get_db)):
    tasks = db.query(Task).all()
    return tasks

## Update (現状タイトルだけ変更)
@router.put("/{task_id}")
def update_task(task_id: int, title: str, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        return {"error": "Task not found"}
    task.title = title
    db.commit()
    return task

## Delete
@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        return {"error": "Task not found"}
    
    db.delete(task)
    db.commit()
    return {"message": "deleted"}