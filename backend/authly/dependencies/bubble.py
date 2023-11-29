from authly.api.api_v2 import http_exceptions
from authly.crud.crud_bubble import BUBBLES_COLLECTION
from authly.interface import bubble
from authly.models import bubble_model
from bson import ObjectId


async def get_bubble_config(bubble_id: str) -> bubble_model.BubbleConfig:
    try:
        object_id = ObjectId(bubble_id)

        status, data = await bubble.get_bubble_data(
            BUBBLES_COLLECTION, object_id
        )
        if status:
            return data
        raise http_exceptions.bubble_id_not_found

    except Exception:
        # Handle the InvalidId exception
        raise http_exceptions.invalid_document_id
