from sqlalchemy import Column, Integer, String, ForeignKey
from ..core.database import Base

class URL(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String(255), index=True)
    status = Column(String(20), default="UNKNOWN")
    response_time = Column(Integer, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))