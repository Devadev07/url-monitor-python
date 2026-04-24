from apscheduler.schedulers.background import BackgroundScheduler
from ..core.database import SessionLocal
from ..services.url_service import URLService
from ..core.logger import logger
import asyncio

scheduler = BackgroundScheduler()


def scheduled_check():
    db = SessionLocal()

    try:
        service = URLService()

        asyncio.run(service.check_all_urls(db))

        logger.info("Scheduled check completed")

    except Exception as e:
        logger.error(f"Scheduler failed: {str(e)}")

    finally:
        db.close()


def start_scheduler():
    if not scheduler.running:
        scheduler.add_job(
            scheduled_check,
            "interval",
            minutes=5,
            id="global_check",
            replace_existing=True
        )

        scheduler.start()