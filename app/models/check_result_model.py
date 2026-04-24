from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from datetime import datetime
from ..core.database import Base

class CheckResult(Base):
    __tablename__ = "check_results"

    id = Column(Integer, primary_key=True, index=True)
    url_id = Column(Integer, ForeignKey("urls.id"))
    status = Column(String(20))
    response_time = Column(Integer, nullable=True)
    checked_at = Column(DateTime, default=datetime.utcnow)
    reason = Column(String(255), nullable=True)