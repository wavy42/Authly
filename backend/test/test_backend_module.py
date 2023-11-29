import os
from unittest.mock import patch
import pytest
from backend import check_dependencies, print_logo, main
from io import StringIO
import sys

ASCII_ART_CONTENT = None


def get_ascii_art_content():
    global ASCII_ART_CONTENT
    if ASCII_ART_CONTENT is None:
        # Get the path to the ASCII art file dynamically
        file_path = os.path.join(os.path.dirname(__file__), "../ascii_art.txt")

        # Read the content of the file
        with open(file_path, "r") as file:
            ASCII_ART_CONTENT = file.read()

    return ASCII_ART_CONTENT


@pytest.fixture
def mock_import_module_success():
    with patch("importlib.import_module") as mock_import_module:
        yield mock_import_module


@pytest.fixture
def mock_import_module_failure(mock_import_module_success):
    mock_import_module_success.side_effect = ImportError
    return mock_import_module_success


def test_check_dependencies_success(mock_import_module_success, caplog):
    dependencies_to_check = ["colorama", "fastapi", "motor"]
    check_dependencies(dependencies_to_check)
    assert not caplog.records


def test_check_dependencies_failure(mock_import_module_failure, capsys):
    dependencies_to_check = ["nonexistent_dependency"]

    # Redirect stdout to capture printed output
    sys.stdout = StringIO()

    with pytest.raises(ImportError) as exc_info:
        # Call the function you want to test
        check_dependencies(dependencies_to_check)

    # Restore stdout
    sys.stdout = sys.__stdout__

    # Check if the expected part of the error message is in the actual message
    expected_part = "The dependency nonexistent_dependency "
    "is not installed or not reachable."
    assert expected_part in str(exc_info.value)


def test_print_logo(capfd):
    ascii_art = get_ascii_art_content()
    with patch("builtins.open", create=True) as mock_open:
        mock_open.return_value.__enter__.return_value.read.return_value = (
            ascii_art
        )
        print_logo("\033[31m")
    captured = capfd.readouterr()
    assert ascii_art in captured.out


def test_main(mock_import_module_success, capfd, caplog):
    # Replace the following with the actual ASCII art content
    ascii_art = get_ascii_art_content()

    with patch("builtins.open", create=True) as mock_open:
        mock_open.return_value.__enter__.return_value.read.return_value = (
            ascii_art
        )
        with patch("backend.os.path.dirname") as mock_dirname:
            mock_dirname.return_value = "../__init__.py"
            main()
