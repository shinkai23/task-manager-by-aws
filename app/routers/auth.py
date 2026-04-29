from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.auth import LoginRequest, TokenResponse
from app.models.user import User
from app.db.deps import get_db
from app.utils.security import verify_password, create_access_token

router = APIRouter("/auth", tags=["auth"])

@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    verify = verify_password(data.password, user.password_hash)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email")
    
    if not verify:
        raise HTTPException(status_code=401, detail="Invalid password")
    
    token = create_access_token({"user_id": data.id})

    return {
        "access_token": token,
        "token_type": "bearer"
    }