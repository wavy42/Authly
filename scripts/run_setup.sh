#!/bin/bash

# Check if Python is installed
if [ -z "$(command -v python3)" ]; then
    echo "Python is not installed. Attempting to install Python..."

    # Install Python (for Debian/Ubuntu-based systems)
    if [ -n "$(command -v apt-get)" ]; then
        sudo apt-get update
        sudo apt-get install -y python3
    else
        echo "Unsupported system. Please install Python manually."
        exit 1
    fi
fi


python3 -m pip install --user pipx
python3 -m pipx ensurepath

python3 -m pip install --user --upgrade pipx

pipx install poetry

poetry install

poetry run python3 -m ./authly/app.py