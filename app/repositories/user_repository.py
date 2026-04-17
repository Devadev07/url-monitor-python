from sqlalchemy.orm import Session
from ..models.user_model import User

class UserRepository:
    def create_user(self, db: Session, username: str, password: str):
        user = User(username=username, password=password)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def get_user_by_username(self, db: Session, username: str):
        return db.query(User).filter(User.username == username).first()