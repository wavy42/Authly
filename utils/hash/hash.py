import hashlib
import json
import logging
import os
from pathlib import Path
import shutil


def clean_pycache(directory: str):
    deleted_directories = []

    for path in Path(directory).rglob("__pycache__"):
        if path.is_dir():
            shutil.rmtree(path)
            deleted_directories.append(str(path))

    return deleted_directories


def pycache_operations(path):
    cleaned_directories = clean_pycache(path)
    print("Deleted pycache directories:")
    for d in cleaned_directories:
        logging.info(f"Removed: {d}")
        print(d)


def check_new_files(directory, expected_hashes, base_path):
    """
    Check for new files in the directory and prompt\
        the user to add their hashes.
    """
    new_files = []
    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            filepath = os.path.relpath(os.path.join(root, filename), base_path)
            if filepath not in expected_hashes:
                new_files.append(filepath)
    return new_files


def check_existing_files(expected_files, base_path):
    """
    Check existing files against their expected hashes.
    """
    for filepath, expected_hash in expected_files.items():
        full_path = os.path.join(base_path, filepath)
        if os.path.exists(full_path):
            with open(full_path, "rb") as file:
                file_hash = hashlib.sha256(file.read()).hexdigest()
                if file_hash != expected_hash:
                    print(f"Hash mismatch" f"for {filepath}. ")
                    user_input = input(
                        "Do you want to update the hash? (y/n): "
                    )
                    if user_input.lower() == "y":
                        expected_files[filepath] = file_hash
                        logging.info(f"Hash updated for {filepath}.")
                        print(f"Hash updated for {filepath}.")
                    else:
                        logging.info(f"Skipping {filepath} hash update")
                        print(f"Skipping {filepath} hash update.")
                else:
                    logging.info(f"Hash match for: {filepath}")
                    print(f"Hash match for" f"{filepath}.")
        else:
            logging.error(f"File {filepath} does not exist.")
            print(f"File {filepath} does not exist.")


def get_file_hash(file_path, base_path):
    hasher = hashlib.sha256()
    with open(os.path.join(base_path, file_path), "rb") as file:
        content = file.read()
        hasher.update(content)
    return hasher.hexdigest()


def check_hash_change(directory_path, base_path):
    if os.path.exists(os.path.join(base_path, "hashes.json")):
        with open(os.path.join(base_path, "hashes.json"), "r") as file:
            expected_files = json.load(file)
    else:
        logging.error("hashes.json not found")
        expected_files = {}

    new_files = check_new_files(directory_path, expected_files, base_path)
    if new_files:
        print("New files found:")
        for f in new_files:
            logging.info(f"new file: {f}")
            print(f)

        user_input = input(
            "Do you want to add all new files to expected files? (a/n): "
        )
        if user_input.lower() == "a":
            logging.info(f"user added all new files ({user_input})")
            for f in new_files:
                file_hash = get_file_hash(f, base_path)
                expected_files[f] = file_hash
                logging.info(
                    f"Added {f} with hash {file_hash} to expected files"
                )
                print(f"Added {f} with hash {file_hash} to expected files.")
        else:
            for f in new_files:
                user_input = input(
                    f"Do you want to add {f} to expected files? (y/n): "
                )
                if user_input.lower() == "y":
                    file_hash = get_file_hash(f, base_path)
                    expected_files[f] = file_hash
                    logging.info(
                        f"Added {f} with hash {file_hash} to expected files"
                    )
                    print(
                        f"Added {f} with hash {file_hash} to expected files."
                    )
    return expected_files


def remove_missing_files(expected_files, base_path):
    missing_files = [
        file_path
        for file_path in expected_files
        if not os.path.exists(os.path.join(base_path, file_path))
    ]
    if missing_files:
        print("Missing files found:")
        for f in missing_files:
            print(f)

        user_input = input(
            "Do you want to remove all missing"
            "files from the expected files? (y/n): "
        )
        if user_input.lower() == "y":
            for f in missing_files:
                expected_files.pop(f, None)
                logging.info(f"Removed {f} from expected files")
        else:
            print("Skipping removal of missing files.")


def hash_operations(directory_path, base_path):
    expected_files = check_hash_change(directory_path, base_path)

    check_existing_files(expected_files, base_path)

    remove_missing_files(expected_files, base_path)

    with open(f"{base_path}/hashes.json", "w") as file:
        json.dump(expected_files, file, indent=4)


if __name__ == "__main__":
    module_directory = os.path.dirname(__file__)
    base_path = os.path.dirname(os.path.abspath(__file__))

    directory_path = os.path.join(base_path, "authly")
    pycache_operations(directory_path)
    hash_operations(directory_path, base_path)
