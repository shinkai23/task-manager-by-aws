from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.auth import LoginRequest, TokenResponse
from app.db.deps import get_db
from app.utils.security import create_access_token
from app.services import user_service
from app.exceptions import UnauthorizedException

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = user_service.authenticate_user(db, data=data)

    token = create_access_token({"user_id": user.id})
    return {
        "access_token": token,
        "token_type": "bearer"
    }