"""
Redis Manager Module

This module defines a RedisManager class for interacting with a Redis server. \
It provides methods to connect to the server, \
    set and retrieve key-value pairs, and close the connection.

Usage:
    from redis_manager import RedisManager

    # Create an instance of RedisManager
    redis_manager = RedisManager(redis_port=6379, redis_db=0,\
        redis_host='localhost')

    # Connect to the Redis server
    success, _, message = redis_manager.connect()

    # Set a key-value pair in Redis
    success, _, message = redis_manager.set(key='example_key',\
        value='example_value')

    # Retrieve the value associated with a key
    success, result, message = redis_manager.get(key='example_key')
    if success:
        print(f"Value for 'example_key': {result}")

    # Close the connection to the Redis server
    success, _, message = redis_manager.close()

Author: Arteii
Date: 25/10/2023
"""
import redis
from redis.exceptions import RedisError, ResponseError
from authly.core.config import application_config as config


class RedisManager:
    def __init__(
        self,
        redis_db: int = config.RedisdbSettings.REDIS_DB,
        redis_port: int = config.RedisdbSettings.REDIS_PORT,
        redis_host: str = config.RedisdbSettings.REDIS_HOST,
    ) -> None:
        """
        Initialize the RedisManager instance.

        :param redis_port: The port to connect to Redis.
        :param redis_db: The Redis database index.
        :param redis_host: The Redis server host (default is "localhost").
        """
        self.redis_client: redis.Redis
        self.host = redis_host
        self.port = redis_port
        self.db = redis_db

    def connect(self) -> bool:
        """
        Connect to the Redis server.

        :return: True if the connection is successful, False otherwise.
        :raises RedisConnectionError: \
            If a connection to Redis cannot be established.
        """
        try:
            self.redis_client = redis.Redis(
                host=self.host, port=self.port, decode_responses=True
            )
        except RedisError as e:
            raise RedisConnectionError(f"Failed to connect to Redis: {e}")
        else:
            return True

    def close(self) -> bool:
        """
        Close the connection to the Redis server.

        :return: True if the connection is closed successfully, \
            False otherwise.
        :raises RedisOperationError: If closing the connection fails.
        """
        try:
            self.redis_client.close()
        except RedisError as e:
            raise RedisOperationError(f"Failed to close Redis connection: {e}")
        else:
            return True

    def set(self, key: str, value: str, expiration_seconds: int = 0) -> bool:
        """
        Set a key-value pair in Redis.

        :param key: The Redis key.
        :param value: The value to set for the key.
        :param expiration_seconds: Expiration time in seconds \
            (default is 0 for no expiration).
        :return: True if the set operation is successful.
        :raises RedisOperationError: If setting the value in Redis fails.
        """
        try:
            if expiration_seconds:
                self.redis_client.setex(key, expiration_seconds, value)
            else:
                self.redis_client.set(key, value)
        except RedisError as e:
            raise RedisOperationError(f"Failed to set value in Redis: {e}")
        else:
            return True

    def get(self, key: str) -> str:
        """
        Get the value associated with a key in Redis.

        :param key: The Redis key.
        :return: The value associated with the key, \
            or None if the key is not found.
        :raises RedisOperationError: \
            If getting the value from Redis fails for other reasons.
        """
        try:
            result = self.redis_client.get(key)
            return str(result) if result is not None else None  # type: ignore
        except ResponseError as e:
            if "no such key" in str(e):
                return None  # type: ignore
            raise RedisOperationError(f"Failed to get value from Redis: {e}")

    def delete(self, key: str) -> bool:
        """
        Delete a key from Redis.

        :param key: The Redis key to delete.
        :return: True if the delete operation is successful.
        :raises RedisOperationError: If deleting the key from Redis fails.
        """
        try:
            self.redis_client.delete(key)
        except RedisError as e:
            raise RedisOperationError(f"Failed to delete key from Redis: {e}")
        else:
            return True

    def exists(self, key: str) -> int:
        """
        Check if a key exists in Redis.

        :param key: The Redis key to check.
        :return: 1 if the key exists, 0 otherwise.
        :raises RedisOperationError: If checking key existence in Redis fails.
        """
        try:
            result = self.redis_client.exists(key)
            return result  # type: ignore
        except RedisError as e:
            raise RedisOperationError(
                f"Failed to check key existence in Redis: {e}"
            )


class RedisConnectionError(Exception):
    pass


class RedisOperationError(Exception):
    pass
