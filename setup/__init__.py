import importlib
import shutil
import subprocess
import time


def install_dependencies(poetry_path):
    try:
        if poetry_path:
            # Check if Poetry is installed
            subprocess.run(
                [poetry_path, "--version"],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            print("Poetry is installed.")

            # Run poetry install
            subprocess.run([poetry_path, "install"], check=True, text=True)
            print("Dependencies installed successfully.")
        else:
            print("Error: Poetry is not installed.")
    except subprocess.CalledProcessError as e:
        print(f"Error: There was an issue installing dependencies. {e.stderr}")


def check_dependencies(dependencies):
    for dependency in dependencies:
        try:
            importlib.import_module(dependency)
        except ImportError:
            return False
    return True


def main():
    poetry_path = shutil.which("poetry")

    dependencies_to_check = ["requests"]

    attempts = 0
    max_attempts = 3
    while attempts < max_attempts:
        if check_dependencies(dependencies_to_check):
            print("All dependencies are satisfied.")
            break
        else:
            print("Some dependencies are missing. Attempting to install...")
            install_dependencies(poetry_path)
            time.sleep(2)  # Optional: Wait for a few seconds before rechecking
            attempts += 1
    else:
        print("Max attempts reached. Aborting.")


if __name__ == "__main__":
    main()
