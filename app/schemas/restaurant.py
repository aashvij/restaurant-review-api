from pydantic import BaseModel, HttpUrl, Field
from datetime import datetime
from typing import Optional

class RestaurantBase(BaseModel):
    restaurant_name: str = Field(..., min_length=1, max_length=100)
    cuisine: str = Field(..., max_length=50)
    address: str = Field(..., max_length=200)
    city: str = Field(..., max_length=100)
    country: str = Field(..., max_length=100)
    phone_number: Optional[str] = Field(None, max_length=20)
    website: Optional[HttpUrl] = None
    zip_code: str = Field(..., max_length=20)

class RestaurantCreate(RestaurantBase):
    pass

class RestaurantResponse(RestaurantBase):
    id: int
    rating: float
    created_at: datetime

    class Config:
        from_attributes = True
