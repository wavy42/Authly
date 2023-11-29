"""
Password Complexity Validation Module

This module provides a function to validate the complexity of a password based\
    on specific requirements, such as minimum length, uppercase letters,\
        lowercase letters, digits, and special characters.

Author: Arteii
Date: 24/10/2023

Usage:
    from validate_password_complexity import validate_password_complexity

    try:
        validated_password = validate_password_complexity("Passw0rd!")
        print(f"Valid password: {validated_password}")
    except ValueError as e:
        print(f"Invalid password: {e}")

The `validate_password_complexity` function checks if a given password meets\
the specified complexity requirements. In this example,\
    the requirements include:
- A minimum length of 8 characters.
- At least one uppercase letter.
- At least one lowercase letter.
- At least one digit.
- At least one special character from the set: @, $, !, %, *, ?, &.

Example:
    Valid: "Passw0rd!", "S@feP@ss"
    Invalid: "12345678", "Password", "special!"
"""

import re
from typing import Tuple, List, Union


def validate_password_complexity(password: str) -> Union[bool, str]:
    rules: List[Tuple[bool, str]] = [
        (len(password) >= 8, "Password must be at least 8 characters long."),
        (
            re.search(r"[A-Z]", password) is not None,
            "Password must contain at least one uppercase letter.",
        ),
        (
            re.search(r"[a-z]", password) is not None,
            "Password must contain at least one lowercase letter.",
        ),
        (
            re.search(r"\d", password) is not None,
            "Password must contain at least one digit.",
        ),
        (
            re.search(r"[@$!%*?&]", password) is not None,
            "Password must contain at least one special character (@$!%*?&).",
        ),
    ]

    failed_rules = [
        (condition, message) for condition, message in rules if not condition
    ]

    if failed_rules:
        return failed_rules[0][1]

    return True
