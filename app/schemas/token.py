from pydantic import BaseModel, Field

class Token(BaseModel):
    """
    Schema for authentication token response.
    """
    access_token: str = Field(
        description="JWT access token",
        example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    )
    token_type: str = Field(
        description="Type of token",
        example="bearer"
    )

class UserBase(BaseModel):
    """
    Base schema for user data.
    """
    username: str = Field(
        description="User's username",
        example="johndoe",
        min_length=3,
        max_length=50
    )
