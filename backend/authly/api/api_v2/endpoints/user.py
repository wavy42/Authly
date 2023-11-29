from authly.dependencies.bubble import get_bubble_config
from authly.models.bubble_model import BubbleConfig
from fastapi import APIRouter, Depends


user = APIRouter()


@user.get("/{bubble_id}")
async def user_router_hello_world(
    config: BubbleConfig = Depends(get_bubble_config),
):
    return {
        "msg": f"Hello World from bubble with id: {config.id}",
        "name": config.name,
    }


@user.post("/create/{bubble_id}")
async def create_user(config: BubbleConfig = Depends(get_bubble_config)):
    pass
    # result = await crud_user.create_new_user(
    #     config.user_document_id,
    # )
