from typing import Dict, List, Union
import json
from pathlib import Path
from .options import OPTIONS

VERSION = OPTIONS["version"]
SERVER_BASE_PATH = Path(OPTIONS["paths"]["server_base"])


def confirm(msg: str, default: bool = False) -> bool:
    """
    Ask the user to confirm an action.

    ```py
    if confirm("Continue?", True):
        print("Ok!")
    else:
        print("Aborting...")
    ```
    """

    try:
        value = input(
            f"{msg} [{'Y/n' if default else 'y/N'}] ").strip().lower()
    except KeyboardInterrupt:
        print()
        raise KeyboardInterrupt
    return value in ["yes", "y"] or (default and not value)


def choice(msg: str, alternatives: List[str], default: int = 0) -> int:
    """
    Display multiple choice dialog to select between a list of alternatives

    ```py
    if choice("What is your favorite color?", ["Red", "Green", "Blue"], 1) == 2:
        print("Ok, blue is your favorite color.")
    ```
    """

    print(msg)

    for i, alternative in enumerate(alternatives):
        print(f"  {alternative}: [{i}]")
    try:
        value = input(f"Enter number: [{default}] ")
        if not value:
            value = default
        else:
            value = int(value)
    except ValueError:
        return -1
    except KeyboardInterrupt:
        print()
        raise KeyboardInterrupt
    if value >= 0 and value < len(alternatives):
        return value
    return -1


def custom_choice(msg: str, default: Union[str, None] = None) -> str:
    """
    Allow to enter any text and returns it
    """

    suffix = ""
    if default:
        suffix = f" [{default}]"
    try:
        value = input(
            f"{msg}{suffix}: ").strip().lower()
    except KeyboardInterrupt:
        print()
        raise KeyboardInterrupt
    return value if value else default
