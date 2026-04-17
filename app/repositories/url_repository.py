from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from ..models.url_model import URL

class URLRepository:
    def create_url(self, db: Session, address: str):
        try:
            url = URL(address=address, status="UNKNOWN")
            db.add(url)
            db.commit()
            db.refresh(url)
            return url
        except IntegrityError:
            db.rollback()
            raise HTTPException(status_code=400, detail="URL already exists")

    def update_status(self, db: Session, url_obj, status, response_time):
        url_obj.status = status
        url_obj.response_time = response_time
        db.commit()
        db.refresh(url_obj)
        return url_obj

    def get_all_urls(self, db):
        return db.query(URL).all()
    
    def create_url(self, db, address, user_id):
        new_url = URL(address=address, user_id=user_id)
        db.add(new_url)
        db.commit()
        db.refresh(new_url)
        return new_url 
    
    def get_urls_by_user(self, db, user_id):
       return db.query(URL).filter(URL.user_id == user_id).all()
