from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserResponse
from app.models.user import User
from app.db.deps import get_db
from app.utils.deps import get_current_user_id
from app.utils.security import hash_password
from app.services import user_service
from app.exceptions import BadRequestException

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserResponse)
def create_user(data: UserCreate, db: Session = Depends(get_db)):
    user = user_service.create_user(db, data=data)

    if not user:
        raise BadRequestException("Email already registered")

    return user

@router.get("/me", response_model=UserResponse)
def get_me(db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    return user_service.get_user_by_id(db, user_id=user_id)