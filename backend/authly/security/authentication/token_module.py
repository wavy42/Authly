import random
import string
from authly.db.redis import RedisManager


def generate_token(len: int = 64) -> str:
    return "".join(random.choices(string.ascii_letters + string.digits, k=len))


def is_key_valid(token: str, redis_manager: RedisManager) -> bool:
    return False if 0 == redis_manager.exists(token) else True


def get_user_id(token: str, redis_manager: RedisManager) -> str:
    return redis_manager.get(token)


def store_token(
    token: str,
    user_id: str,
    redis_manager: RedisManager,
    expiration_time_minutes: int = 1440,
) -> bool:
    _ = redis_manager.set(
        token, user_id, expiration_seconds=expiration_time_minutes * 60
    )

    return True


def get_new_token(
    user_id: str,
    redis_manager: RedisManager,  # type: ignore
    expiration_time_minutes: int = 1440,
    token: str = "",
) -> str:
    """
    - generate_token()
    - is_key_valid()
    - store_token()
    - cloe connection
    """
    new_token = generate_token()
    if token:
        new_token = token

    if is_key_valid(new_token, redis_manager):
        get_new_token(user_id, redis_manager, expiration_time_minutes)

    store_token(new_token, user_id, redis_manager, expiration_time_minutes)

    return new_token
