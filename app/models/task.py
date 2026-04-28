from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, Enum
from sqlalchemy.orm import relationship
from app.db.session import Base
from app.schemas.enums import TaskStatus, TaskPriority
from datetime import datetime

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String(100), nullable=False)
    description = Column(Text)
    status = Column(Enum(TaskStatus))
    priority = Column(Enum(TaskPriority))
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="tasks")