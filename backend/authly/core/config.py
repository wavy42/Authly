"""
This is a Python script for handling configuration settings using Pydantic.
It reads a JSON file and validates it against a predefined Pydantic model.
"""

import os
import json
from pydantic_settings import BaseSettings
from authly.core.utils.log import Logger, LogLevel


############################################################
#                       JSON FORMAT                        #
############################################################


class LoggingSettings(BaseSettings):
    """
    Configuration settings for logging.

    Attributes:
        LOG_LEVEL (str): The log level for the application.\
            Default is "INFO".
            Possible values include "DEBUG", "INFO",\
                "WARNING", "ERROR", and "CRITICAL".
        LOG_FILE_PATH (str): The file path for the log file.\
            Default is "app.log".
            The log file will be created at the specified path.
    """

    LOG_LEVEL: str = "INFO"
    LOG_FILE_PATH: str = "app.log"


class Debug_Authly(BaseSettings):
    DEBUG: bool = False
    LoggingSettings: LoggingSettings


class API_V1(BaseSettings):
    """
    Configuration settings for API version 1.

    Attributes:
        API_V1_ACTIVE (bool):\
            Whether to use API version 1. Default is True.
        API_V1_ROUTE (str):\
            The route for API version 1. Default is "/v1".
    """

    API_V1_ACTIVE: bool = True
    API_V1_ROUTE: str = "/v1"


class API_V2(BaseSettings):
    """
    Configuration settings for API version 2.

    Attributes:
        API_V2_ACTIVE (bool):\
            Whether to use API version 2. Default is False.
        API_V2_ROUTE (str):\
            The route for API version 2. Default is "/v2".
    """

    API_V2_ACTIVE: bool = False
    API_V2_ROUTE: str = "/v2"
    # not yet available


class API(BaseSettings):
    """
    Configuration settings for the backend.authly.api.

    Attributes:
        API_ROUTE (str):\
            The base route where the API is located. Default is "/api".
        API_V1 (API_V1):\
            Configuration settings for API version 1.
        API_V2 (API_V2):\
            Configuration settings for API version 2.
    """

    API_ROUTE: str = "/api"
    API_V1: API_V1
    API_V2: API_V2


class ArgonHashingAlgorithm(BaseSettings):
    """
    Configuration settings for the Argon2 password hashing algorithm.

    Attributes:
        TIME_COST (int):\
            The number of iterations (time cost) for Argon2.\
                Default is 1048576 (2^20).
        MEMORY_COST (int):\
            The memory usage (in MiB) for Argon2.\
                Default is 65536 MiB.
        PARALLELISM (int):\
            The number of threads (parallelism) used during Argon2 execution.\
                Default is 4.
        HASH_LEN (int):\
            The length of the resulting hash in bytes.\
                Default is 16 bytes.
        SALT_LEN (int):\
            The length of the salt used in bytes.\
                Default is 32 bytes.
        ENCODING (str):\
            The character encoding used for hashing, e.g., 'utf-8'.
    """

    TIME_COST: int = 12
    MEMORY_COST: int = 256
    PARALLELISM: int = 4
    SALT_LEN: int = 32
    HASH_LEN: int = 64
    ENCODING: str = "utf-8"


class PasswordConfig(BaseSettings):
    """
    Configuration settings for password hashing and password policies.

    Attributes:
        USE_PASSWORD_HASHING (bool):\
            Whether to use password hashing.
        HASHING_ALGORITHM (HashingAlgorithmTypes):\
            The selected password hashing algorithm.
        BcryptHashingAlgorithm (BcryptHashingAlgorithm):\
            Configuration settings for Bcrypt.
        ArgonHashingAlgorithm (ArgonHashingAlgorithm):\
            Configuration settings for Argon2.
        DEFAULT_PASSWORD_MIN_LENGTH (int):\
            The default minimum password length. Default is 11.
        DEFAULT_PASSWORD_MAX_LENGTH (int):\
            The default maximum password length. Default is 50.
    """

    USE_PASSWORD_HASHING: bool = True
    ArgonHashingAlgorithm: ArgonHashingAlgorithm
    DEFAULT_PASSWORD_MIN_LENGTH: int = 11
    DEFAULT_PASSWORD_MAX_LENGTH: int = 50


class MongodbSettings(BaseSettings):
    """
    Configuration settings for connecting to MongoDB.

    Attributes:
        MONGODB_HOST (str):\
            The MongoDB host.
        MONGODB_PORT (int):\
            The MongoDB port.
        DB_NAME (str):\
            The name of the MongoDB database.
        MONGODB_USERNAME (str):\
            Your MongoDB username (if required).
        MONGODB_PASSWORD (str):\
            Your MongoDB password (if required).
        MONGODB_USE_SSL (bool):\
            Whether to use SSL/TLS for communication.
        MONGODB_AUTH_MECHANISM (str):\
            The authentication mechanism.
        MONGODB_MAX_POOL_SIZE (int):\
            The maximum connection pool size.
        MONGODB_MIN_POOL_SIZE (int):\
            The minimum connection pool size.
        MONGODB_MAX_IDLE_TIME_MS (int):\
            The maximum time connections can remain idle.
        MONGODB_WAIT_QUEUE_TIMEOUT_MS (int):\
            The wait queue timeout.
        MONGODB_SERVER_SELECTION_TIMEOUT_MS (int):\
            The server selection timeout.
        MONGODB_READ_CONCERN (str):\
            The read concern.
        MONGODB_WRITE_CONCERN (str):\
            The write concern.
        MONGODB_RETRY_WRITES (bool):\
            Whether to retry writes.
        MONGODB_CONNECT_TIMEOUT_MS (int):\
            The connection timeout.
        MONGODB_SOCKET_TIMEOUT_MS (int):\
            The socket timeout.
    """

    MONGODB_URL: str = "mongodb://localhost:27017"
    MONGODB_NAME: str = "Authly"
    MONGODB_USERNAME: str
    MONGODB_PASSWORD: str
    MONGODB_USE_SSL: bool = False
    MONGODB_AUTH_MECHANISM: str = "SCRAM-SHA-256"
    MONGODB_MAX_POOL_SIZE: int = 100
    MONGODB_MIN_POOL_SIZE: int = 1
    MONGODB_MAX_IDLE_TIME_MS: int = 10000
    MONGODB_WAIT_QUEUE_TIMEOUT_MS: int = 2000
    MONGODB_SERVER_SELECTION_TIMEOUT_MS: int = 30000
    MONGODB_READ_CONCERN: str = "local"
    MONGODB_WRITE_CONCERN: str = "local"
    MONGODB_RETRY_WRITES: bool = True
    MONGODB_CONNECT_TIMEOUT_MS: int = 20000
    MONGODB_SOCKET_TIMEOUT_MS: int = 30000


class RedisdbSettings(BaseSettings):
    """
    Settings class for configuring the Redis database connection.

    read more about redis:
    https://redis.io/docs/

    Attributes:
        REDIS_HOST (str): The Redis host address. Default is "localhost".
        REDIS_PORT (int): The Redis port number. Default is 6379.
        REDIS_DB (int): The Redis database number or index. Default is 0.
    """

    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0


class SessionManagerSettings(BaseSettings):
    """
    Configuration settings for the session manager.

    Attributes:
        ALLOW_COOKIE_LOGIN (bool):\
            Allow login via the cookie field.
        DEFAULT_PATH (str):\
            The default path for cookies.
        DEFAULT_STORE_IP_WITH_SESSION (bool):\
            Store session with IP restriction.
        DEFAULT_MAX_NUMBER_OF_IPS (int):\
            The number of allowed IPs per session.
        DEFAULT_DELETE_ON_LOGIN_ERROR (bool):\
            Delete session on malicious login attempts.
        DEFAULT_MAX_AGE_SECONDS (int):\
            The maximum age for a session in seconds.\
                Default is 86400 (24 hours).
        DEFAULT_SECURE (bool):\
            Whether the cookie should only be sent over HTTPS.
    """

    ALLOW_COOKIE_LOGIN: bool = True
    DEFAULT_PATH: str = "/"
    DEFAULT_STORE_IP_WITH_SESSION: bool = True
    DEFAULT_MAX_NUMBER_OF_IPS: int = 1
    DEFAULT_DELETE_ON_LOGIN_ERROR: bool = True
    DEFAULT_MAX_AGE_SECONDS: int = 86400
    DEFAULT_SECURE: bool = True


class AppConfig(BaseSettings):
    """
    Configuration settings for the application.

    Attributes:
        API (API):\
            Configuration settings for the backend.authly.api.
        PasswordConfig (PasswordConfig):\
            Configuration settings for password hashing and policies.
        MongodbSettings (MongodbSettings):\
            Configuration settings for connecting to MongoDB.
        SessionManagerSettings (SessionManagerSettings):\
            Configuration settings for the session manager.
    """

    Debug_Authly: Debug_Authly
    API: API
    PasswordConfig: PasswordConfig
    MongodbSettings: MongodbSettings
    RedisdbSettings: RedisdbSettings
    SessionManagerSettings: SessionManagerSettings


def check_file(file_name):
    # Get the directory of the current script or module
    script_directory = os.path.dirname(os.path.realpath(__file__))

    # Move up one directory to reach the parent directory
    parent_directory = os.path.abspath(
        os.path.join(script_directory, os.pardir, os.pardir, os.pardir)
    )
    # Construct the relative path to the JSON file in the parent directory
    json_file_path = os.path.join(parent_directory, "config", file_name)

    Logger.log(LogLevel.DEBUG, "JSON file path:", f"{json_file_path}")

    # Load JSON file
    with open(json_file_path, encoding="utf-8") as f:
        data = json.load(f)
    return data


def validate_config(data):
    return_data = AppConfig(**data)
    return return_data


config_data = check_file("backend_config.json")
application_config = validate_config(config_data)
