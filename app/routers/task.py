from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate
from app.services import task_service
from app.utils.deps import get_current_user_id

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/", response_model=TaskResponse)
def create_task(
    data: TaskCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    return task_service.create_task(db, user_id=user_id, data=data)


@router.get("/", response_model=list[TaskResponse])
def get_tasks(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    return task_service.get_tasks(db, user_id=user_id)


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    return task_service.get_task(db, task_id=task_id, user_id=user_id)


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    data: TaskUpdate,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    return task_service.update_task(db, task_id=task_id, user_id=user_id, data=data)


@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    task_service.delete_task(db, task_id=task_id, user_id=user_id)
    return {"message": "deleted"}
