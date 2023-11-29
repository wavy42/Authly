from typing import Tuple, Union
from authly.db.mongo import MongoDBManager
from authly.core.utils.log import Logger, LogLevel
from authly.models import (
    application_model,
    bubble_model,
    key_model,
    user_model,
)
from bson import InvalidDocument, ObjectId


async def create_bubble_in_collection(
    collection: str,
    config: Union[
        user_model.UserDB, application_model.ApplicationDB, key_model.KeyDB
    ],
) -> str:
    mongo_manager = MongoDBManager(collection)
    try:
        status, data, details = await mongo_manager.insert_document(
            config.model_dump()
        )
        Logger.log(
            LogLevel.DEBUG,
            "create_bubble_in_collections:",
            status,
            data,
            details,
        )
    except Exception:
        raise

    else:
        return str(data)

    finally:
        try:
            await mongo_manager.close_connection()

        except Exception:
            raise


async def create_bubble_config(
    collection_name,
    config: bubble_model.CreateBubble,
) -> Tuple[bool, str]:
    mongo_manager = MongoDBManager(collection_name)
    try:
        status, data, details = await mongo_manager.insert_document(
            config.model_dump()
        )
        Logger.log(
            LogLevel.DEBUG,
            "create_bubble_in_collections:",
            status,
            data,
            details,
        )
        new_document_id = str(data)

    except Exception:
        raise

    finally:
        try:
            await mongo_manager.close_connection()

        except Exception:
            raise

    return status, new_document_id


async def update_bubble_config(
    collection_name,
    config: bubble_model.BubbleConfig,
) -> Tuple[bool, str]:
    mongo_manager = MongoDBManager(collection_name)
    try:
        print(config.model_dump())
        status, data, details = await mongo_manager.update_one_document(
            {"_id": ObjectId(config.id)}, {**config.model_dump()}
        )
        Logger.log(
            LogLevel.DEBUG,
            "update_bubble_config:",
            status,
            data,
            details,
        )
        new_document_id = str(data)

    except Exception:
        raise

    finally:
        try:
            await mongo_manager.close_connection()

        except Exception:
            raise

    return status, new_document_id


async def get_bubble_data(
    collection_name: str,
    bubble_id: ObjectId,
) -> Tuple[bool, bubble_model.BubbleConfig]:
    mongo_manager = MongoDBManager(collection_name)
    try:
        status, data, details = await mongo_manager.find_one(
            {"_id": bubble_id}
        )
        Logger.log(
            LogLevel.DEBUG,
            "get_bubble_data:",
            status,
            data,
            details,
        )
        if not data:
            raise Exception(f"invalid data: ({data})")
    except InvalidDocument:
        raise

    except Exception:
        raise

    finally:
        try:
            await mongo_manager.close_connection()

        except Exception:
            raise

    return status, bubble_model.BubbleConfig(**data)


async def delete_bubble_in_collection():
    pass


async def delete_bubble_config():
    pass
