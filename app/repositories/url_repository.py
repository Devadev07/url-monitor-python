from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from ..models.url_model import URL

class URLRepository:

    def create_url(self, db: Session, address: str, user_id: int):
        try:
            new_url = URL(
                address=address,
                status="UNKNOWN",
                user_id=user_id
            )

            db.add(new_url)
            db.commit()
            db.refresh(new_url)

            return new_url

        except IntegrityError:
            db.rollback()
            raise HTTPException(status_code=400, detail="URL already exists")

    def update_status(self, db, url_obj, status, response_time, reason):
        url_obj.status = status
        url_obj.response_time = response_time
        url_obj.reason = reason
        
        db.commit()
        db.refresh(url_obj)

        return url_obj

    def get_all_urls(self, db):
        return db.query(URL).all()

    def get_urls_by_user(self, db, user_id):
        return db.query(URL).filter(URL.user_id == user_id).all()