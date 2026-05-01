from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.models.task import Task
from app.db.deps import get_db
from app.utils.deps import get_current_user_id
from app.services import task_service

router = APIRouter(prefix="/tasks")
 
# CRUD の実装を行う

## Create
@router.post("/", response_model=TaskResponse)
def create_task(data: TaskCreate, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    task_service(data, user_id, db)

## Read 一件取得
@router.get("/{task_id}", response_model=TaskResponse)
def read_task(task_id: int, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    task = task_service.get_task(task_id, user_id, db)
    if not task:
        raise HTTPException(status=404, detail="Task not found")
    return task

## Read 一覧取得
@router.get("/", response_model=list[TaskResponse])
def read_tasks(user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    tasks = task_service.get_tasks(user_id, db)
    return tasks

## Update (現状タイトルだけ変更)
@router.put("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, data: TaskUpdate, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    task = task_service.get_task(task_id, user_id, db)
    if not task:
        raise HTTPException(status=404, detail="Task not found")
    return task_service.update_task(task_id, data, db)

## Delete
@router.delete("/{task_id}")
def delete_task(task_id: int, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    task = task_service.get_task(task_id, user_id, db)
    if not task:
        raise HTTPException(status=404, detail="Task not found")
    
    task_service.delete_task(task, db)
    return {"message": "deleted"}