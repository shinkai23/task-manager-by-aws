from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserResponse
from app.models.user import User
from app.db.deps import get_db
from app.utils.deps import get_current_user_id
from app.utils.security import hash_password
from app.services import user_service

router = APIRouter(prefix="/users")

@router.post("/", response_model=UserResponse)
def create_user(data: UserCreate, db: Session = Depends(get_db)):
    user = user_service.create_user(
        data.username, 
        data.email,
        data.password,
        db
    )

    if not user:
        raise HTTPException(status_code=400, detail = "Email already registered")

    return user

@router.get("/me", response_model=UserResponse)
def get_me(user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    return user_service.get_user_by_id(user_id)