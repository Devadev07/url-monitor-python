from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session

from ..schemas.url_schema import URLCreate
from ..services.url_service import URLService
from ..core.database import SessionLocal
from ..models.url_model import URL
from ..models.check_result_model import CheckResult
from ..models.user_model import User
from ..core.security import verify_token

router = APIRouter()
service = URLService()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    if not authorization:
        raise HTTPException(status_code=401, detail="Token missing")

    token = authorization.split(" ")[1]

    payload = verify_token(token)

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    username = payload.get("sub")

    user = db.query(User).filter(User.username == username).first()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user


@router.post("/add-url")
def add_url(
    url: URLCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return service.add_url(
        db,
        url.address,
        current_user.id,
        url.check_interval
    )


@router.post("/check-url/{url_id}")
async def check_url(
    url_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    url_obj = db.query(URL).filter(URL.id == url_id).first()

    if not url_obj:
        raise HTTPException(status_code=404, detail="URL not found")

    return await service.check_url(db, url_obj)


@router.post("/check-all")
async def check_all(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return await service.check_all_urls(db)


@router.get("/user-urls")
def get_user_urls(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return service.get_user_urls(db, current_user.id)


@router.delete("/delete-url/{url_id}")
def delete_url(
    url_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    url_obj = db.query(URL).filter(URL.id == url_id).first()

    if not url_obj:
        raise HTTPException(status_code=404, detail="URL not found")

    db.query(CheckResult).filter(CheckResult.url_id == url_id).delete()

    db.delete(url_obj)
    db.commit()

    return {"message": "URL deleted successfully"}