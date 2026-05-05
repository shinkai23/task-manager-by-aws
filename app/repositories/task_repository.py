from sqlalchemy.orm import Session

from app.models.task import Task


def create(db: Session, task: Task):
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def get_by_id(db: Session, task_id: int, user_id: int):
    return db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()


def get_all(db: Session, user_id: int):
    return db.query(Task).filter(Task.user_id == user_id).all()


def update(db: Session, task: Task, data):
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)
    return task


def delete(db: Session, task: Task):
    db.delete(task)
    db.commit()
