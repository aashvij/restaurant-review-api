from fastapi import FastAPI
from .api.auth import router as auth_router
from .api.user import router as user_router
from .api.restaurant import router as restaurant_router
from .api.review import router as review_router
from fastapi.openapi.utils import get_openapi

app = FastAPI()
app.include_router(auth_router, tags=["auth"])
app.include_router(user_router)
app.include_router(restaurant_router)
app.include_router(review_router)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="My Custom API",
        version="1.0.0",
        description="This is a custom OpenAPI schema",
        routes=app.routes,
    )
    
    # Custom documentation modifications
    openapi_schema["info"]["x-logo"] = {
        "url": "https://yourwebsite.com/logo.png"
    }
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
