"""
Username Validation Module

This module provides a function to validate the format of a username\
    based on a regular expression pattern.

Author: Arteii
Date: 24/10/2023

Usage:
    from validate_username import validate_username

    try:
        validated_username = validate_username("abc#1234")
        print(f"Valid username: {validated_username}")
    except ValueError as e:
        print(f"Invalid username: {e}")

The `validate_username` function checks if a given username matches the\
    specified format: three or more letters followed by a '#' character and\
        four numbers (e.g., abc#1234).

Example:
    Valid: "abc#1234", "xyz#5678"
    Invalid: "abc1234", "12#abcd", "abc#12345"

"""

import re


def validate_username(
    value: str, pattern: str = r"^[a-zA-Z]{3,}#[0-9]{4}$"
) -> bool:
    """
    Validate the username format using a regular expression.

    Args:
        value (str): The username to validate.
        pattern (str): The regex pattern for validation.

    Returns:
        bool: The result of the validation.
    """
    return bool(re.fullmatch(pattern, value))
