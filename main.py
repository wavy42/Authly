import argparse
from setup.app import main as setup


def main() -> None:
    parser = argparse.ArgumentParser(description="Your program description.")

    # Add command-line arguments
    parser.add_argument("-f", "--file", help="Full path to the config file")
    parser.add_argument("--web", help="URL for web-based config")

    args = parser.parse_args()

    if args.web:
        setup.from_web(args.web)
    elif args.file:
        setup.from_file(args.file)
    else:
        setup.config_wizard()


if __name__ == "__main__":
    main()
