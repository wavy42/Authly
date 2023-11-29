from authly.api.api_v2.endpoints.user import user
from authly.api.api_v2.endpoints.admin import admin
from fastapi import APIRouter

api_v2_router = APIRouter()

tags_metadata = [
    {
        "name": "users",
        "description": "Operations with users."
        "The **login** logic is also here.",
    },
    {
        "name": "admin",
        "description": "Manage items. So _fancy_ they have their own docs.",
        "externalDocs": {
            "description": "Items external docs",
            "url": "https://example.com/",
        },
    },
]

api_v2_router.include_router(user, tags=["users"], prefix="/user")
api_v2_router.include_router(admin, tags=["admin"], prefix="/admin")


@api_v2_router.get("/")
async def api_router_hello_world():
    return {"msg": "Hello World"}
