from sqlalchemy.exc import IntegrityError
from ..repositories.user_repository import UserRepository
from ..core.security import verify_password, create_access_token
from ..models.user_model import User
import bcrypt


class UserService:
    def __init__(self):
        self.repository = UserRepository()

    def signup(self, db, user):
        hashed = bcrypt.hashpw(
            user.password.encode(),
            bcrypt.gensalt()
        ).decode()

        return self.repository.create_user(
            db,
            user.username,
            hashed
        )

    def login(self, db, user_data):
        user = db.query(User).filter(User.username == user_data.username).first()

        if not user:
           return {"message": "User not found"}

        if not verify_password(user_data.password, user.password):
           return {"message": "Invalid password"}

        token = create_access_token({"sub": user.username})

        return {
            "access_token": token,
            "token_type": "bearer",
            "id": user.id
        }