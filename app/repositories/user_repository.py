from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from ..models.user_model import User

class UserRepository:

  def create_user(self, db, username, password):
    try:
        new_user = User(
            username=username,
            password=password
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {
            "message": "Signup successful"
        }

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

  def get_by_username(self, db, username):
    return db.query(User).filter(User.username == username).first()
