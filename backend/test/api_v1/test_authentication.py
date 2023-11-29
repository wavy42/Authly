import pytest
from authly.core.db.redis_crud import RedisManager
from authly.api.api_v1.authentication import token_module


@pytest.fixture
def redis_manager():
    # Set up your Redis manager here or use a mock
    # For simplicity, you can use a local Redis server for testing
    return RedisManager(redis_db=2, redis_host="localhost", redis_port=6379)


def test_generate_token():
    token = token_module.generate_token()
    assert len(token) == 64
    assert token.isalnum()


def test_is_key_valid(redis_manager):
    redis_manager.connect()
    token = token_module.generate_token()
    assert not token_module.is_key_valid(token, redis_manager)
    token_module.store_token(token, "user_id", redis_manager)
    assert token_module.is_key_valid(token, redis_manager)
    redis_manager.close()


def test_get_user_id(redis_manager):
    token = token_module.generate_token()
    user_id = "user_id"
    redis_manager.connect()
    token_module.store_token(token, user_id, redis_manager)
    assert token_module.get_user_id(token, redis_manager) == user_id
    redis_manager.close()


def test_store_token(redis_manager):
    token = token_module.generate_token()
    user_id = "user_id"
    expiration_time_minutes = 10
    redis_manager.connect()
    assert token_module.store_token(
        token, user_id, redis_manager, expiration_time_minutes
    )
    assert token_module.is_key_valid(token, redis_manager)
    redis_manager.close()


def test_get_new_token(redis_manager):
    redis_manager.connect()
    user_id = "user_id"
    token = token_module.get_new_token(user_id, redis_manager)
    assert token_module.is_key_valid(token, redis_manager)
    assert token_module.get_user_id(token, redis_manager) == user_id
    redis_manager.close()


def test_get_new_token_existing(redis_manager):
    redis_manager.connect()
    user_id = "user_id"
    exisitng = "exisiting"
    token_module.store_token(exisitng, user_id, redis_manager)
    token = token_module.get_new_token(user_id, redis_manager, token=exisitng)
    assert token_module.is_key_valid(token, redis_manager)
    assert token_module.get_user_id(token, redis_manager) == user_id
    redis_manager.close()
