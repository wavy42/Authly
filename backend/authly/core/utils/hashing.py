"""
Password Hashing and Verification Module

This module provides classes and methods for\
    password hashing and verification using
Bcrypt and Argon2 hashing algorithms.\
    It also includes a Hasher class for handling
password hashing and verification using various algorithms.

Author: Arteii
Date: 24/10/2023
"""
from typing import Optional

import argon2
from authly.core.config import application_config

config = application_config.PasswordConfig  # type: ignore
argon_config = config.ArgonHashingAlgorithm


def get_argon2_manager(
    time_cost: int = argon_config.TIME_COST,
    memory_cost: int = argon_config.MEMORY_COST,
    parallelism: int = argon_config.PARALLELISM,
    hash_len: int = argon_config.HASH_LEN,
    salt_len: int = argon_config.SALT_LEN,
    encoding: str = argon_config.ENCODING,
) -> argon2.PasswordHasher:
    """
    Get an instance of the Argon2 password hasher with the specified\
        configuration.

    Args:
        time_cost (int): The number of iterations to use (time cost).
        memory_cost (int): The amount of memory to use in kibibytes\
            (memory cost).
        parallelism (int): The degree of parallelism to use (parallelism).
        hash_len (int): The length of the hash to produce (hash length).
        salt_len (int): The length of the randomly generated salt\
            (salt length).
        encoding (str): The character encoding to use.

    Returns:
        argon2.PasswordHasher: An instance of the Argon2 password hasher.
    """
    return argon2.PasswordHasher(
        time_cost, memory_cost, parallelism, hash_len, salt_len, encoding
    )


def verify_password(
    password: str,
    stored_hash: str,
    argon2_manager: Optional[argon2.PasswordHasher] = None,
) -> bool:
    """
    Verify a password against a stored Argon2 hash.

    Args:
        password (str): The password to be verified.
        stored_hash (str): The stored Argon2 hash.
        argon2_manager (argon2.PasswordHasher): Optional Argon2 manager.

    Returns:
        bool: True if the password is valid, False otherwise.
    """
    argon2_manager = argon2_manager or get_argon2_manager()
    try:
        argon2_manager.verify(stored_hash, password)

    except argon2.exceptions.VerificationError:
        return False

    else:
        return True


def get_password_hash(
    password: str,
    argon2_manager: Optional[argon2.PasswordHasher] = None,
) -> str:
    """
    Hash a password using Argon2.

    Args:
        password (str): The password to be hashed.
        argon2_manager (argon2.PasswordHasher): Optional Argon2 manager.

    Returns:
        str: The Argon2 hash of the password.
    """
    argon2_manager = argon2_manager or get_argon2_manager()
    return argon2_manager.hash(password)
