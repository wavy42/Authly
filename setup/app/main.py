from setup.app.core import file_setup, web_setup, wizard


def from_web(url: str) -> None:
    web_setup.setup_from_web(url)


def from_file(file: str) -> None:
    file_setup.setup_from_file(file)


def config_wizard():
    wizard.main()
