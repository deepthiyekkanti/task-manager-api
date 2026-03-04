from sqlalchemy.orm import Session
from fastapi import HTTPException
from models import User
from schemas import UserCreate
from auth.security import hash_password


class UserService:
    def signup(self, db: Session, user: UserCreate) -> User:
        existing = db.query(User).filter(User.email == user.email).first()
        if existing:
            raise HTTPException(status_code=400, detail="User already exists")

        new_user = User(email=user.email, password_hash=hash_password(user.password))
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    def get_me(self, db: Session, user_id: int) -> User:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user