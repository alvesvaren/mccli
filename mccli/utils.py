from typing import Dict, List, Union


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
        return False
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
    except (KeyboardInterrupt, ValueError):
        print()
        return -1
    if value >= 0 and value < len(alternatives):
        return value
    return -1
