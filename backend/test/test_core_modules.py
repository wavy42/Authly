import pytest
from typing import Any, Literal, Union
from authly.core import (
    password_validation,
    username_validation,
    object_id,
    hashing,
    log,
)
from bson import ObjectId


class TestPasswordValidation:
    @pytest.mark.parametrize(
        "password, expected_result",
        [
            ("1234567", "Password must be at least 8 characters long."),
            (
                "passwithoutuppercase",
                "Password must contain at least one uppercase letter.",
            ),
            (
                "PASSWITHOUTLOWERCASE",
                "Password must contain at least one lowercase letter.",
            ),
            (
                "PAss@@!!!WITHOutDIGITS",
                "Password must contain at least one digit.",
            ),
            (
                "P4SSW1TH3V3RYTH1ngbutsp3z14l",
                "Password must contain at least "
                "one special character (@$!%*?&).",
            ),
            ("V3ryS3cureP@Ss", True),
            ("5aYtH/Mh.O4LQkSqQ?l;h$df%'J]Ex1^qT", True),
        ],
    )
    def test_password_complexity_validation(
        self,
        password: Literal[
            "1234567",
            "passwithoutuppercase",
            "PASSWITHOUTLOWERCASE",
            "PAss@@!!!WITHOutDIGITS",
            "P4SSW1TH3V3RYTH1ngbutsp3z14l",
            "V3ryS3cureP@Ss",
            "5aYtH/Mh.O4LQkSqQ?l;h$df%'J]Ex1^qT",
        ],
        expected_result: Union[bool, str],
    ):
        result = password_validation.validate_password_complexity(password)
        assert result == expected_result

    def test_short_password(self):
        short_password = "Short!"
        result = password_validation.validate_password_complexity(
            short_password
        )
        assert "Password must be at least 8 characters long." in result


class TestUsernameValidation:
    @pytest.mark.parametrize(
        "username, expected_result",
        [
            ("abc#1234", True),
            ("xyz#5678", True),
            ("abc1234", False),
            ("12#abcd", False),
            ("abc#12345", False),
        ],
    )
    def test_username_validation(
        self,
        username: Literal[
            "abc#1234", "xyz#5678", "abc1234", "12#abcd", "abc#12345"
        ],
        expected_result: bool,
    ):
        result = username_validation.validate_username(username)
        assert result == expected_result


class TestConvertObjectIdToStr:
    @pytest.fixture
    def sample_data(self):
        return {
            "_id": ObjectId(),
            "name": "John Doe",
            "age": 30,
            "address": {"_id": ObjectId(), "city": "New York", "state": "NY"},
        }

    def test_convert_object_id_to_str(self, sample_data: dict[str, Any]):
        converted_data = object_id.convert_object_id_to_str(sample_data)

        # Check if _id is converted to id
        assert "id" in converted_data
        assert "_id" not in converted_data

        # Check if ObjectId is converted to string
        assert isinstance(converted_data["id"], str)

        # Check if nested dictionaries are processed correctly
        address_data = converted_data.get("address")
        assert address_data is not None
        assert "id" in address_data
        assert "_id" not in address_data
        assert isinstance(address_data["id"], str)

    def test_convert_object_id_to_str_with_none(self):
        result = object_id.convert_object_id_to_str(None)
        assert result is None

    def test_convert_object_id_to_str_with_non_dict(self):
        result = object_id.convert_object_id_to_str("some_string")
        assert result == "some_string"

    def test_convert_str_to_object_id_dict(self):
        input_data = {
            "id": "60a32e70b4381534cf59b8e4",
            "name": "John Doe",
            "age": 30,
        }

        expected_output = {
            "_id": ObjectId("60a32e70b4381534cf59b8e4"),
            "name": "John Doe",
            "age": 30,
        }

        result = object_id.convert_str_to_object_id(input_data)
        assert result == expected_output


class TestLogger:
    def test_logger_main(self):
        result = log.main()
        assert result is True


class TestHasher:
    def test_verify_password(self):
        # Generate a hash for a known password for testing
        password = "test_password"
        stored_hash = hashing.get_password_hash(password)

        # Test valid password
        assert hashing.verify_password(password, stored_hash)

        # Test invalid password
        assert not hashing.verify_password("wrong_password", stored_hash)

        # Test mismatched password
        assert not hashing.verify_password("mismatched_password", stored_hash)

    def test_get_password_hash(self):
        password = "test_password"
        hashed_password = hashing.get_password_hash(password)

        # Ensure the hashed password is not the same as the original password
        assert hashed_password != password

        # Verify the hashed password
        assert hashing.verify_password(password, hashed_password)

        # Test mismatched password
        assert not hashing.verify_password(
            "mismatched_password", hashed_password
        )
