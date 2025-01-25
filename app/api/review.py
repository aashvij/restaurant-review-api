from fastapi import APIRouter, HTTPException
from ..schemas.review import ReviewCreate, ReviewResponse
from typing import Dict, List
from datetime import datetime
from .restaurant import restaurants_db  # Import the restaurants database
from .user import users_db  # Import the users database

router = APIRouter(
    prefix="/reviews",
    tags=["reviews"]
)

# In-memory storage
reviews_db: Dict[int, dict] = {}
current_id = 1

def update_restaurant_rating(restaurant_id: int):
    """Calculate and update the average rating for a restaurant"""
    restaurant_reviews = [
        review for review in reviews_db.values() 
        if review['restaurant_id'] == restaurant_id
    ]
    
    if not restaurant_reviews:
        restaurants_db[restaurant_id]['rating'] = 0.0
        return
    
    avg_rating = sum(review['rating'] for review in restaurant_reviews) / len(restaurant_reviews)
    restaurants_db[restaurant_id]['rating'] = round(avg_rating, 1)

@router.post("/", response_model=ReviewResponse)
def create_review(review: ReviewCreate):
    global current_id

    # Validate restaurant and user exist (as before - lines 35-41) ...

    existing_review_id = None
    existing_review = None
    for review_id, r in reviews_db.items(): # Iterate through reviews_db to find existing review
        if r['user_id'] == review.user_id and r['restaurant_id'] == review.restaurant_id:
            existing_review_id = review_id
            existing_review = r
            break

    if existing_review:
        # Update existing review
        existing_review['rating'] = review.rating
        existing_review['comment'] = review.comment
        existing_review['created_at'] = datetime.utcnow() # Or add 'updated_at' field and update it
        review_dict = existing_review # Use the updated review dictionary for response
    else:
        # Create new review (as before - lines 61-71)
        review_dict = review.model_dump()
        review_dict['id'] = current_id
        review_dict['created_at'] = datetime.utcnow()
        reviews_db[current_id] = review_dict
        current_id += 1

    update_restaurant_rating(review.restaurant_id)
    return review_dict

@router.get("/{review_id}", response_model=ReviewResponse)
def get_review(review_id: int):
    if not isinstance(review_id, int) or review_id < 1:
        raise HTTPException(
            status_code=400, 
            detail="Invalid review ID"
        )
    if review_id not in reviews_db:
        raise HTTPException(status_code=404, detail="Review not found")
    return reviews_db[review_id]

@router.delete("/{review_id}")
def delete_review(review_id: int):
    if review_id not in reviews_db:
        raise HTTPException(status_code=404, detail="Review not found")
    
    # Get restaurant_id before deleting the review
    restaurant_id = reviews_db[review_id]['restaurant_id']
    
    # Delete the review
    del reviews_db[review_id]
    
    # Update restaurant rating
    update_restaurant_rating(restaurant_id)
    
    return {"message": "Review deleted"}

@router.get("/restaurant/{restaurant_id}", response_model=List[ReviewResponse])
def get_restaurant_reviews(restaurant_id: int):
    restaurant_reviews = [
        review for review in reviews_db.values() 
        if review['restaurant_id'] == restaurant_id
    ]
    return restaurant_reviews
