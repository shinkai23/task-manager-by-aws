from sqlalchemy.orm import Session
from app.models.user import User
from app.utils.security import hash_password, verify_password

def create_user(username: str, email: str, password: str, db: Session):
    existing = db.query(User).filter(User.email == email).first()
    if existing:
        return None

    user = User(
        username=username,
        email=email,
        password_hash=hash_password(password)
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def authenticate_user(email: str, password: str, db: Session):
    user = db.query(User).filter(User.email == email).first()

    if not user:
        return None
    
    if not verify_password(password, user.password_hash):
        return None
    
    return user

def get_user_by_id(user_id: int, db: Session):
    return db.query(User).filter(User.id == user_id).first()
