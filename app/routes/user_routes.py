from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..schemas.user_schema import UserCreate
from ..services.user_service import UserService
from ..core.database import SessionLocal

router = APIRouter()

service = UserService()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    return service.signup(db, user)

@router.post("/login")
def login(user: UserCreate, db: Session = Depends(get_db)):
    return service.login(db, user)