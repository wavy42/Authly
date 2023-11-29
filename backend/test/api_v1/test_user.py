from authly.api.api_v1.db.connect import get_mongo_manager
import pytest
from bson import ObjectId
from authly.api.api_v1.user.managment import (
    get_user_data_by_id,
    get_user_data_by_email,
    get_user_data_by_username,
    MongoDBManager,
    LogLevel,
    Logger,
    convert_object_id_to_str,
)


@pytest.fixture
def mongo_client():
    mongo_client = get_mongo_manager("TESTER")

    return mongo_client


@pytest.mark.asyncio
async def test_get_user_data_by_id(mongo_client):
    user_data = {"username": "test_user"}
    await mongo_client.write_manager.insert_document(data=user_data)

    user_id = str(user_data["_id"])
    result = await get_user_data_by_id(user_id, mongo_client)

    assert result == convert_object_id_to_str(user_data)


@pytest.mark.asyncio
async def test_get_user_data_by_email(mongo_client):
    user_data = {"username": "test_user", "email": "test@example.com"}
    await mongo_client.write_manager.insert_document(data=user_data)

    email = "test@example.com"
    found, result = await get_user_data_by_email(email, mongo_client)

    assert found == True
    assert result.get("email") == email


@pytest.mark.asyncio
async def test_get_user_data_by_username(mongo_client):
    user_data = {"username": "TestUser"}
    await mongo_client.write_manager.insert_document(data=user_data)

    username = "test_user"
    found, result = await get_user_data_by_username(username, mongo_client)

    assert found is True
    assert result.get("username") == username
