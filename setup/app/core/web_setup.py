import json
import os
import tempfile
import requests


def download_config_from_web(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error downloading config from {url}: {e}")
        return None


def save_config_to_temp_file(config):
    temp_dir = tempfile.gettempdir()
    temp_file_path = os.path.join(temp_dir, "temp_config.json")

    with open(temp_file_path, "w") as file:
        file.write(json.dumps(config, indent=2))

    return temp_file_path


def setup_from_web(url):
    config = download_config_from_web(url)

    if config:
        temp_file_path = save_config_to_temp_file(config)
        print(f"Config downloaded and saved to {temp_file_path}")
        # Add the rest of your setup logic using the downloaded config
    else:
        print("Failed to download and save the config. Setup aborted.")
