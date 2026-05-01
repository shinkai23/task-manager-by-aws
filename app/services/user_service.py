from sqlalchemy.orm import Session
from app.models.user import User
from app.utils.security import hash_password, verify_password

def create_user(db: Session, *, data):
    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        return None

    user = User(
        username=data.username,
        email=data.email,
        password_hash=hash_password(data.password)
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def authenticate_user(db: Session, *, data):
    user = db.query(User).filter(User.email == data.email).first()

    if not user:
        return None
    
    if not verify_password(data.password, user.password_hash):
        return None
    
    return user

def get_user_by_id(db: Session, *, user_id: int):
    return db.query(User).filter(User.id == user_id).first()
