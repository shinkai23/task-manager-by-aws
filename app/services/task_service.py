from sqlalchemy.orm import Session
from app.models.task import Task
from app.exceptions import NotFoundException

def create_task(db: Session, *, user_id: int, data):
    task = Task(**data.dict(), user_id=user_id)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def get_tasks(db: Session, *, user_id: int,):
    return db.query(Task).filter( Task.user_id == user_id).all()

def get_task(db: Session, *, task_id: int, user_id: int):
    task = db.query(Task).filter(
        Task.id == task_id, 
        Task.user_id == user_id
        ).first()
    if not task:
        raise NotFoundException("Task not found")

def update_task(db: Session, *, task_id: int, user_id: int, data):
    task = get_task(db, task_id=task.id, user_id=user_id)
    for key, value in data.dict(exclude_unset=True).items():
        setattr(task, key, value)
    
    db.commit()
    db.refresh(task)
    return task

def delete_task(db:Session, *, task):
    db.delete(task)
    db.commit()
    return True