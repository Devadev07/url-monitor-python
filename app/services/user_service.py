from sqlalchemy.exc import IntegrityError
from ..repositories.user_repository import UserRepository
from ..core.security import hash_password, verify_password
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

    def login(self, db, user):
        db_user = self.repository.get_user_by_username(
            db,
            user.username
        )

        if not db_user:
            return {"message": "User not found"}

        if bcrypt.checkpw(
            user.password.encode(),
            db_user.password.encode()
        ):
            return {
                "message": "Login success",
                "id": db_user.id,
                "username": db_user.username
            }

        return {"message": "Wrong password"}