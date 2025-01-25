from fastapi import APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends
from ..schemas.token import Token
from ..core.security import create_access_token
from typing import Annotated

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
    responses={404: {"description": "Not found"}},
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Simplified user database (replace with real database)
FAKE_DB = {
    "testuser": {"username": "testuser", "password": "testpass"}
}

@router.post("/login", response_model=Token)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    """
    Authenticate a user and return a JWT token.

    Args:
        form_data: OAuth2 password request form containing:
            - username: The user's username
            - password: The user's password

    Returns:
        Token: An object containing the access token and token type

    Raises:
        HTTPException: 401 error if credentials are invalid
    """
    user = FAKE_DB.get(form_data.username)
    if not user or form_data.password != user["password"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(user["username"])
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/logout")
async def logout(
    token: Annotated[str, Depends(oauth2_scheme)]
) -> dict[str, str]:
    """
    Logout a user by invalidating their token.

    Args:
        token: JWT token from the Authorization header

    Returns:
        dict: A message confirming successful logout
    """
    return {"message": "Successfully logged out"}
