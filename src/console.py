class Colors:
    CYAN = '\033[96m'
    YELLOW = '\033[93m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    MAGENTA = '\033[95m'
    BLUE = '\033[94m'
    RESET = '\033[0m'


def printInfo(text: str):
    print(f"{Colors.CYAN}{text}{Colors.RESET}")


def printDebug(text: str):
    print(f"{Colors.MAGENTA}{text}{Colors.RESET}")


def printSuccess(text: str):
    print(f"{Colors.GREEN}{text}{Colors.RESET}")


def printError(text: str):
    print(f"{Colors.RED}{text}{Colors.RESET}")


def printWarn(text: str):
    print(f"{Colors.YELLOW}{text}{Colors.RESET}")
