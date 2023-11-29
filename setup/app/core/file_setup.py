import json


def load_config_from_file(file_path):
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from {file_path}: {e}")
        return None


def setup_from_file(file_path):
    config = load_config_from_file(file_path)

    if config:
        print(f"Config loaded from file: {file_path}")
        # Add the rest of your setup logic using the loaded config
    else:
        print("Failed to load the config. Setup aborted.")
