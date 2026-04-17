from ..repositories.url_repository import URLRepository
from ..repositories.check_result_repository import CheckResultRepository
from .monitor_service import MonitorService
from ..core.logger import logger
from ..models.url_model import URL

class URLService:
    def __init__(self):
        self.repository = URLRepository()
        self.monitor = MonitorService()
        self.check_repo = CheckResultRepository()

    def add_url(self, db, address, user_id):
        existing = db.query(URL).filter(
          URL.address == address,
          URL.user_id == user_id
        ).first()

        if existing:
            return {"message": "URL already exists"}

        new_url = URL(
          address=address,
          status="UNKNOWN",
         user_id=user_id
        )
        db.add(new_url)
        db.commit()
        db.refresh(new_url)

        return new_url

    def check_url(self, db, url_obj):
        status, response_time = self.monitor.check_url(url_obj.address)

        self.repository.update_status(db, url_obj, status, response_time)

        self.check_repo.save_result(
            db,
            url_obj.id,
            status,
            response_time
        )

        logger.info(
        f"Checked URL: {url_obj.address}, Status: {status}, Response: {response_time}ms"
        )
        return url_obj

    def check_all_urls(self, db):
        urls = self.repository.get_all_urls(db)

        for url in urls:
            self.check_url(db, url)

        return urls
    
    def get_user_urls(self, db, user_id):
        return self.repository.get_urls_by_user(db, user_id)