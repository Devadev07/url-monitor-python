from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from ..schemas.user_schema import UserCreate, UserLogin
from ..services.user_service import UserService
from ..core.database import SessionLocal
from ..core.security import verify_token

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
def login(user: UserLogin, db: Session = Depends(get_db)):
    return service.login(db, user)

def protected_route(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Token missing")

    token = authorization.split(" ")[1]

    payload = verify_token(token)

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return payload