import asyncio

from authly.core.db.redis_crud import RedisManager
from authly.config import application_config
from authly.core.log import Logger, LogLevel

redis_config = application_config.RedisdbSettings  # type: ignore
REDIS_HOST = redis_config.REDIS_HOST
REDIS_PORT = redis_config.REDIS_PORT
REDIS_DB = redis_config.REDIS_DB


# Create instances of the database managers
redis = RedisManager(
    redis_host=REDIS_HOST, redis_port=REDIS_PORT, redis_db=REDIS_DB
)


# Test function to check the Redis operations
async def async_redis_operations() -> dict:
    test_results = {}

    # Connect to Redis
    connected = redis.connect()
    if connected:
        test_results["connection"] = "Passed"
    if not connected:
        Logger.log(LogLevel.CRITICAL, "Failed to connect to Redis:", connected)
        return test_results

    # Perform a write operation
    key = "test_key"
    value = "test_value"
    write_result = redis.set(key, value)
    if write_result:
        test_results["write_operation"] = "Passed"
        Logger.log(LogLevel.DEBUG, "Value set successfully in Redis")
    else:
        test_results["write_operation"] = "Failed"
        Logger.log(LogLevel.ERROR, "Failed to set value in Redis")

    # Perform a read operation
    read_result = redis.get(key)
    if read_result:
        test_results["read_operation"] = "Passed"
        Logger.log(
            LogLevel.DEBUG, f"Value retrieved from Redis: {read_result}"
        )
    else:
        test_results["read_operation"] = "Failed"
        Logger.log(LogLevel.ERROR, "Failed to retrieve value from Redis")

    # Perform a delete operation
    delete_result = redis.delete(key)
    if delete_result:
        test_results["delete_operation"] = "Passed"
        Logger.log(LogLevel.DEBUG, "Key deleted successfully from Redis")
    else:
        test_results["delete_operation"] = "Failed"
        Logger.log(LogLevel.ERROR, "Failed to delete key from Redis")

    # Close the Redis connection
    closed = redis.close()
    if closed:
        test_results["close_connection"] = "Passed"
        Logger.log(LogLevel.DEBUG, "Redis connection closed successfully")
    else:
        test_results["close_connection"] = "Failed"
        Logger.log(LogLevel.ERROR, "Failed to close Redis connection")

    return {"Redis": [test_results]}


async def print_results():
    Logger.tests(await async_redis_operations())  # type: ignore


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(print_results())
