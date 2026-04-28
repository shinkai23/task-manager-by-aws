from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from app.schemas.enums import TaskStatus, TaskPriority

class TaskBase(BaseModel):
    title: str = Field(..., max_length=100)
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.todo
    priority: TaskPriority = TaskPriority.medium

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=100)
    description: Optional[str]  = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None

class TaskResponse(TaskBase):
    id: int

    model_config = ConfigDict(from_attributes=True)