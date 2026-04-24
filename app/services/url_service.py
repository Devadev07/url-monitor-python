from ..repositories.url_repository import URLRepository
from ..repositories.check_result_repository import CheckResultRepository
from .monitor_service import MonitorService
from ..core.logger import logger
from ..models.url_model import URL
import asyncio

class URLService:
    def __init__(self):
        self.repository = URLRepository()
        self.monitor = MonitorService()
        self.check_repo = CheckResultRepository()

    def add_url(self, db, address, user_id, check_interval):
        existing = db.query(URL).filter(
            URL.address == address,
            URL.user_id == user_id
        ).first()

        if existing:
            return {"message": "URL already exists"}

        new_url = URL(
            address=address,
            status="UNKNOWN",
            user_id=user_id,
            check_interval=check_interval
        )

        db.add(new_url)
        db.commit()
        db.refresh(new_url)

        return new_url

    async def check_url(self, db, url_obj):
        status, response_time, reason = await self.monitor.check_single_url(url_obj.address)

        self.repository.update_status(db, url_obj, status, response_time, reason)

        self.check_repo.save_result(
            db,
            url_obj.id,
            status,
            response_time,
            reason
        )

        logger.info(
            f"Checked URL: {url_obj.address}, Status: {status}, Response: {response_time}ms"
        )

        return {
            "id": url_obj.id,
            "address": url_obj.address,
            "status": url_obj.status,
            "response_time": url_obj.response_time,
            "reason": url_obj.reason
        }

    async def check_all_urls(self, db):
        urls = self.repository.get_all_urls(db)

        tasks = [self.monitor.check_single_url(url.address) for url in urls]

        results = await asyncio.gather(*tasks, return_exceptions=True)

        for url, result in zip(urls, results):
            if isinstance(result, Exception):
                continue

            status, response_time, reason = result

            self.repository.update_status(db, url, status, response_time, reason)

            self.check_repo.save_result(
                db,
                url.id,
                status,
                response_time,
                reason
            )

            logger.info(
                f"Checked URL: {url.address}, Status: {status}, Response: {response_time}ms"
            )

        return {
            "message": "All URLs checked successfully",
            "checked_count": len(urls),
            "urls": [
                {
                    "id": url.id,
                    "address": url.address,
                    "status": url.status,
                    "response_time": url.response_time,
                    "reason": url.reason
                }
                for url in urls
            ]
        }

    def get_user_urls(self, db, user_id):
        return self.repository.get_urls_by_user(db, user_id)