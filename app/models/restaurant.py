from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from .user import Base

class Restaurant(Base):
    __tablename__ = "restaurants"

    id = Column(Integer, primary_key=True, index=True)
    restaurant_name = Column(String(100), nullable=False, index=True)
    rating = Column(Float, default=0.0)
    cuisine = Column(String(50))
    address = Column(String(200))
    city = Column(String(100))
    country = Column(String(100))
    phone_number = Column(String(20))
    website = Column(String(200))
    zip_code = Column(String(20))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
