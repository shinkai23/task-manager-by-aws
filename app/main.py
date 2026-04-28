from fastapi import FastAPI
from app.db.session import engine, Base
from app.routers import task, user
app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(task.router)
app.include_router(user.router)