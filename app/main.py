from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.db.session import engine, Base
from app.routers import task, user, auth
from app.exceptions import AppException


app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(task.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.code,
                "message": exc.message
            }
        },
    )