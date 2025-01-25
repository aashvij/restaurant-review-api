from pydantic import BaseModel, Field
from datetime import datetime

class ReviewBase(BaseModel):
    rating: float = Field(..., ge=1, le=5)
    comment: str = Field(..., max_length=500)
    restaurant_id: int
    user_id: int

class ReviewCreate(ReviewBase):
    pass

class ReviewResponse(ReviewBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
