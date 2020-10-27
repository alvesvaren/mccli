

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
