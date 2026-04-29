from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.models.task import Task
from app.db.deps import get_db
from app.utils.deps import get_current_user_id

router = APIRouter(prefix="/tasks")
 
# CRUD の実装を行う

## Create
@router.post("/", response_model=TaskResponse)
def create_task(data: TaskCreate, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    task = Task(**data.dict(), user_id=user_id)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

## Read 一件取得
@router.get("/{task_id}", response_model=TaskResponse)
def read_task(task_id: int, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()
    if not task:
        raise HTTPException(status=404, detail="Task not found")
    return task

## Read 一覧取得
@router.get("/", response_model=list[TaskResponse])
def read_tasks(user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    tasks = db.query(Task).filter(Task.user_id == user_id).all()
    return tasks

## Update (現状タイトルだけ変更)
@router.put("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, data: TaskUpdate, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()
    if not task:
        raise HTTPException(status=404, detail="Task not found")
    for key, value in data.dict(exclude_unset=True).items():
        setattr(task, key, value)
    db.commit()
    db.refresh(task)
    return task

## Delete
@router.delete("/{task_id}")
def delete_task(task_id: int, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()
    if not task:
        raise HTTPException(status=404, detail="Task not found")
    
    db.delete(task)
    db.commit()
    return {"message": "deleted"}