from enum import Enum

class TaskStatus(str, Enum):
    todo = "todo"
    doing = "doing"
    done = "done"

class TaskPriority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"