from sqlalchemy.orm import Session
from app.models.user import User
from app.repositories import user_repository
from app.utils.security import hash_password, verify_password
from app.exceptions import NotFoundException, BadRequestException, UnauthorizedException

def create_user(db: Session, *, data):
    existing = user_repository.get_by_email(db, data.email)
    
    if existing:
        raise BadRequestException("Email already registered")

    user = User(
        username=data.username,
        email=data.email,
        password_hash=hash_password(data.password)
    )

    return user_repository.create(db, user)

def authenticate_user(db: Session, *, data):
    user = user_repository.get_by_email(db, data.email)

    if not user:
        raise UnauthorizedException("Invalid credentials")
    
    if not verify_password(data.password, user.password_hash):
        raise UnauthorizedException("Invalid credentials")
    
    return user

def get_user_by_id(db: Session, *, user_id: int):
    user = user_repository.get_by_id(db, user_id)

    if not user:
        raise NotFoundException("User not found")
    
    return user
