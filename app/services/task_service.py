from sqlalchemy.orm import Session

from app.exceptions import NotFoundException
from app.models.task import Task
from app.repositories import task_repository


def create_task(db: Session, *, user_id: int, data):
    task = Task(**data.dict(), user_id=user_id)
    return task_repository.create(db, task)


def get_tasks(db: Session, *, user_id: int):
    return task_repository.get_all(db, user_id)


def get_task(db: Session, *, task_id: int, user_id: int):
    task = task_repository.get_by_id(db, task_id, user_id)
    if not task:
        raise NotFoundException("Task not found")
    return task


def update_task(db: Session, *, task_id: int, user_id: int, data):
    task = get_task(db, task_id=task_id, user_id=user_id)
    return task_repository.update(db, task, data)


def delete_task(db: Session, *, task_id: int, user_id: int):
    task = get_task(db, task_id=task_id, user_id=user_id)
    task_repository.delete(db, task)
