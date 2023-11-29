from authly.api.api_v1.db.connect import get_redis_manager
from authly.core.db.redis_crud import RedisManager
import pytest


@pytest.fixture
def redis_manager() -> RedisManager:
    """
    Fixture to create an instance of RedisManager for testing.
    """
    redis_manager = get_redis_manager(
        redis_port=6379, redis_db=0, redis_host="localhost"
    )
    return redis_manager


def test_connect(redis_manager):
    success = redis_manager.connect()
    assert success is True
    redis_manager.close()


def test_set_and_get(redis_manager):
    redis_manager.connect()

    key = "test_key"
    value = "test_value"

    # Set a key-value pair
    success = redis_manager.set(key=key, value=value)
    assert success is True

    # Retrieve the value associated with the key
    result = redis_manager.get(key=key)
    assert result == value

    redis_manager.close()


def test_delete(redis_manager):
    redis_manager.connect()
    key = "test_key"
    value = "test_value"

    # Set a key-value pair
    redis_manager.set(key=key, value=value)

    # Delete the key
    success = redis_manager.delete(key=key)
    assert success is True

    # Verify that the key no longer exists
    exists = redis_manager.exists(key=key)
    assert exists == 0
    redis_manager.close()


def test_close(redis_manager):
    redis_manager.connect()
    success = redis_manager.close()
    assert success is True
