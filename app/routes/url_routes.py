from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..schemas.url_schema import URLCreate
from ..services.url_service import URLService
from ..core.database import SessionLocal
from ..models.url_model import URL
from fastapi import HTTPException
from ..models.check_result_model import CheckResult

router = APIRouter()
service = URLService()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/add-url")
def add_url(url: URLCreate, db: Session = Depends(get_db)):
    return service.add_url(db, url.address, url.user_id)


@router.post("/check-url/{url_id}")
def check_url(url_id: int, db: Session = Depends(get_db)):
    url_obj = db.query(URL).filter(URL.id == url_id).first()

    if not url_obj:
        raise HTTPException(status_code=404, detail="URL not found")

    return service.check_url(db, url_obj)


@router.post("/check-all")
def check_all(db: Session = Depends(get_db)):
    return service.check_all_urls(db)


@router.get("/user-urls/{user_id}")
def get_user_urls(user_id: int, db: Session = Depends(get_db)):
    return service.get_user_urls(db, user_id)

@router.delete("/delete-url/{url_id}")
def delete_url(url_id: int, db: Session = Depends(get_db)):
    url_obj = db.query(URL).filter(URL.id == url_id).first()

    if not url_obj:
        raise HTTPException(status_code=404, detail="URL not found")

    db.query(CheckResult).filter(CheckResult.url_id == url_id).delete()

    db.delete(url_obj)
    db.commit()

    return {"message": "URL deleted successfully"}