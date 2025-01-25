from fastapi import APIRouter, HTTPException

from app.models.user import UserRole
from ..schemas.user import UserCreate, UserResponse
from typing import Dict, List
from datetime import datetime

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

# In-memory storage
users_db: Dict[int, dict] = {}
current_id = 1

@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate):
    global current_id
    
    # Check for existing username
    if any(u['username'] == user.username for u in users_db.values()):
        print("Current users in DB:", [(u['id'], u['username']) for u in users_db.values()])
        raise HTTPException(status_code=400, detail="Username already exists")
    
    # Create new user
    user_dict = user.model_dump() # pydantic to dict
    user_dict['id'] = current_id
    user_dict['role'] = UserRole.USER
    user_dict['created_at'] = datetime.utcnow()  # Add creation timestamp
    
    users_db[current_id] = user_dict
    current_id += 1
    
    return user_dict

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    return users_db[user_id]

@router.delete("/{user_id}")
def delete_user(user_id: int):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    del users_db[user_id]
    return {"message": "User deleted"}
