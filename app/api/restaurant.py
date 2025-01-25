from fastapi import APIRouter, HTTPException, Query
from ..schemas.restaurant import RestaurantCreate, RestaurantResponse
from typing import Dict, List, Optional
from datetime import datetime

router = APIRouter(
    prefix="/restaurants",
    tags=["restaurants"]
)

# In-memory storage
restaurants_db: Dict[int, dict] = {}
current_id = 1

@router.post("/", response_model=RestaurantResponse)
def create_restaurant(restaurant: RestaurantCreate):
    global current_id
    
    # Validate unique restaurant name
    if any(r['restaurant_name'].lower() == restaurant.restaurant_name.lower() 
           for r in restaurants_db.values()):
        raise HTTPException(
            status_code=400, 
            detail="Restaurant with this name already exists"
        )
    
    # Create new restaurant
    restaurant_dict = restaurant.model_dump()
    restaurant_dict['id'] = current_id
    restaurant_dict['rating'] = 0.0
    restaurant_dict['created_at'] = datetime.utcnow()
    
    restaurants_db[current_id] = restaurant_dict
    current_id += 1
    
    return restaurant_dict

@router.get("/{restaurant_id}", response_model=RestaurantResponse)
def get_restaurant(restaurant_id: int):
    if restaurant_id not in restaurants_db:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return restaurants_db[restaurant_id]

@router.delete("/{restaurant_id}")
def delete_restaurant(restaurant_id: int):
    if restaurant_id not in restaurants_db:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    del restaurants_db[restaurant_id]
    return {"message": "Restaurant deleted"}

@router.get("/", response_model=List[RestaurantResponse])
def get_restaurants(
    cuisine: Optional[str] = None,
    city: Optional[str] = None,
    min_rating: Optional[float] = Query(None, ge=0, le=5),
    sort_by: Optional[str] = Query(None, enum=["rating", "name", "created_at"]),
    order: Optional[str] = Query("asc", enum=["asc", "desc"])
):
    # Validate min_rating range
    if min_rating is not None and not 0 <= min_rating <= 5:
        raise HTTPException(
            status_code=400, 
            detail="min_rating must be between 0 and 5"
        )
    
    filtered_restaurants = list(restaurants_db.values())
    
    # Apply filters with case-insensitive validation
    if cuisine:
        filtered_restaurants = [
            r for r in filtered_restaurants 
            if r['cuisine'].lower() == cuisine.lower()
        ]
    
    if city:
        filtered_restaurants = [
            r for r in filtered_restaurants 
            if r['city'].lower() == city.lower()
        ]
    
    if min_rating is not None:
        filtered_restaurants = [
            r for r in filtered_restaurants 
            if r['rating'] >= min_rating
        ]
    
    # Apply sorting with validation
    if sort_by:
        reverse = order.lower() == "desc"
        if sort_by == "name":
            filtered_restaurants.sort(
                key=lambda x: x['restaurant_name'].lower(),
                reverse=reverse
            )
        elif sort_by == "rating":
            filtered_restaurants.sort(
                key=lambda x: x['rating'],
                reverse=reverse
            )
        elif sort_by == "created_at":
            filtered_restaurants.sort(
                key=lambda x: x['created_at'],
                reverse=reverse
            )
    
    return filtered_restaurants
