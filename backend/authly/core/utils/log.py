import datetime
import inspect
from enum import Enum, auto


from colorama import init, Fore

init(autoreset=True)  # Initialize colorama

application = "Authly"


def footer(COL: str = Fore.WHITE):
    print(f"{COL}|> " + "-" * 50 + f"{Fore.RESET}\n")


def banner(
    main_col: str,
    main_text: str,
    filename: str,
    function: str,
    line: int,
    time: str,
    application: str = application,
):
    print(
        f"{main_col}|> --- {Fore.LIGHTCYAN_EX}{application}{main_col}"
        f" ---- [{main_text}] ---- [{Fore.YELLOW}{time}{Fore.RESET}"
        f"{main_col}] --- [{Fore.BLACK}{filename}{main_col}] --- "
        f"[{Fore.BLUE}{function}{main_col}] --- "
        f"[{Fore.LIGHTYELLOW_EX}{line}{main_col}]"
    )


def format_value(value):
    value_upper = str(value).upper()
    if value_upper == "TRUE":
        return f"{Fore.GREEN}TRUE   {Fore.RESET}"
    elif value_upper == "FALSE":
        return f"{Fore.RED}FALSE  {Fore.RESET}"
    elif value_upper == "FAILED":
        return f"{Fore.RED}FAILED {Fore.RESET}"
    elif value_upper == "PASSED":
        return f"{Fore.GREEN}PASSED {Fore.RESET}"
    elif value_upper == "WARNING":
        return f"{Fore.YELLOW}WARNING{Fore.RESET}"
    else:
        return str(value)


def print_sublist(
    COL,
    item_value: str = "",
    max_item_length: str = "",
    item_key: str = "",
):
    print(
        f"{COL}|{Fore.RESET}   - "
        f"{str(format_value(item_value)).ljust(max_item_length)}"
        f"   {item_key.ljust(15)}"
    )


class LogLevel(Enum):
    INFO = auto()
    WARNING = auto()
    ERROR = auto()
    CRITICAL = auto()
    DEBUG = auto()
    TESTS = auto()


class Logger:
    LOG_LEVEL_COLORS = {
        LogLevel.INFO: "BLUE",
        LogLevel.WARNING: "YELLOW",
        LogLevel.ERROR: "MAGENTA",
        LogLevel.CRITICAL: "RED",
        LogLevel.DEBUG: "CYAN",
        LogLevel.TESTS: "WHITE",
    }
    LOG_LEVEL_NAMES = {
        LogLevel.INFO: "INFO",
        LogLevel.WARNING: "WARNING",
        LogLevel.ERROR: "ERROR",
        LogLevel.CRITICAL: "CRITICAL ERROR",
        LogLevel.DEBUG: "DEBUG",
        LogLevel.TESTS: "TESTS",
    }
    output_debug_log: bool = False
    disable_log: bool = False

    @staticmethod
    def debug_log(level: bool = False):
        Logger.output_debug_log = level

    @staticmethod
    def disable(level: bool = False):
        print("Logger disabled for testing")
        Logger.disable_log = level

    @staticmethod
    def log(level: LogLevel = LogLevel.INFO, *args):
        if Logger.disable_log:
            pass

        NAME = Logger.LOG_LEVEL_NAMES.get(level, "INFO")
        color = Logger.LOG_LEVEL_COLORS.get(level, "WHITE")
        COL = getattr(Fore, color)

        caller_frame = inspect.currentframe().f_back
        caller_info = inspect.getframeinfo(caller_frame)
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if args:
            banner(
                main_col=COL,
                main_text=NAME,
                filename=caller_info.filename,
                function=caller_info.function,
                line=caller_info.lineno,
                time=current_time,
            )

        for arg in args[0:]:
            print(f"{COL}|{Fore.RESET}  {str(arg)}")
        if len(args) > 1:
            footer(COL)
        if len(args) <= 1:
            print("\n")

    def tests(*args, format: bool = True):
        NAME = "TESTS"
        COL = Fore.WHITE
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        caller_frame = inspect.currentframe().f_back
        caller_info = inspect.getframeinfo(caller_frame)

        if args:
            banner(
                main_col=COL,
                main_text=NAME,
                filename=caller_info.filename,
                function=caller_info.function,
                line=caller_info.lineno,
                time=current_time,
            )

        if format and args and isinstance(args[0], dict):
            for key, value in args[0].items():
                if isinstance(value, list):
                    print(f"{COL}| {Fore.RESET}{key} Tests:")
                    for sublist in value:
                        max_item_length = max(
                            len(str(sublist[item])) for item in sublist
                        )
                        for item_key, item_value in sublist.items():
                            print_sublist(
                                COL, item_value, max_item_length, item_key
                            )
                else:
                    print(f"{COL}| {Fore.RESET}{key}: {format_value(value)}")

        else:
            for arg in args[0:]:
                print(f"{COL}|{Fore.RESET}  {str(arg)}")

        if len(args) > 1 or (
            args and isinstance(args[0], dict) and len(args[0]) > 1
        ):
            footer(COL)


# Example usage of the custom_logger function
def main() -> bool:
    Logger.log(
        LogLevel.DEBUG,
        "this is a log with jsut one line.",
    )
    Logger.log(
        LogLevel.DEBUG,
        "This is the first line of the log.",
        "This is the second line of the log.",
        "This is the third line of the log.",
    )
    Logger.log(
        LogLevel.ERROR,
        "This is the first line of the log.",
        "This is the second line of the log.",
        "This is the third line of the log.",
    )
    Logger.log(
        LogLevel.WARNING,
        "This is the first line of the log.",
        "This is the second line of the log.",
        "This is the third line of the log.",
    )
    Logger.log(
        LogLevel.INFO,
        "This is the first line of the log.",
        "This is the second line of the log.",
        "This is the third line of the log.",
    )
    Logger.log(
        LogLevel.CRITICAL,
        "This is the first line of the log.",
        "This is the second line of the log.",
        "This is the third line of the log.",
    )
    Logger.tests(
        {
            "TestTester": "failed",
            "Main Test": [
                {"Test1": "True"},
                {"Test2": "False"},
                {"Test3": "Passed"},
                {"Test4": "Failed"},
                {"Test5": "warninG"},
                {"Test6": "asdasd"},
            ],
        }
    )
    Logger.tests({"TestTester": "failed"})

    Logger.disable(True)
    Logger.log(
        LogLevel.CRITICAL,
        "This is the first line of the log.",
        "This is the second line of the log.",
        "This is the third line of the log.",
    )
    Logger.disable(False)
    Logger.log(
        LogLevel.DEBUG,
        "This is the first line of the log.",
        "This is the second line of the log.",
        "This is the third line of the log.",
    )
    Logger.debug_log(True)
    Logger.log(
        LogLevel.DEBUG,
        "This is the first line of the log.",
        "This is the second line of the log.",
        "This is the third line of the log.",
    )
    return True
