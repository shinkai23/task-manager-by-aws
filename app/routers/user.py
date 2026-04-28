from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserResponse
from app.models.user import User
from app.db.deps import get_db
from app.utils.security import hash_password

router = APIRouter(prefix="/users")

@router.post("/", response_model=UserResponse)
def create_user(data: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.emails == data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail = "Email already registered")
    
    hashed_password = hash_password(data.password)

    user = User(
        username = data.username,
        email = data.email,
        password_hash = hashed_password
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user