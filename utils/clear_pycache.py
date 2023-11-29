import logging
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


if __name__ == "__main__":
    pycache_operations("./backend/")
