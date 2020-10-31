from io import FileIO
from typing import Dict, List, Union
from enum import Enum
import requests
import json
from pathlib import Path

with open(Path(__file__).parent.joinpath("options.json").resolve()) as file:
    OPTIONS: dict = json.load(file)
    URLS: Dict[str, str] = OPTIONS["urls"]
    PAPER_BASE_URL = URLS["papermc"].rstrip("/")


class ServerProvider(Enum):
    """
    """
    VANILLA = "vanilla"
    PAPERMC = "papermc"
    SPIGOT = "spigot"


class ServerType(Enum):
    SNAPSHOT = "snapshot"
    RELEASE = "release"


class ServerVersion():
    def __init__(self, name: str, provider: ServerProvider, url: str = None):
        self.name = name
        self.provider = provider
        self._url = url

    @property
    def url(self) -> str:
        """
        Get the download url for the server binary
        """
        if not self._url:
            self._url = self._get_url()
        return self._url

    def __repr__(self):
        return f"<ServerVersion name='{self.name}' type='{self.provider}'>"

    def download(self) -> bytes:
        """
        Retrun a file object containing the downloaded server binary

        Usage: 
        ```py
        with open("server.jar", "wb") as file:
            file.write(serverVersion.download())
        ```
        """
        return requests.get(self.url).content

    def _get_url(self) -> str:
        """
        Internal function to fetch url, needs to be implemented in order to be used 
        """
        raise NotImplementedError(
            "This type of server version does not support download urls")


class VanillaVersion(ServerVersion):
    def __init__(self, name: str, manifest: dict):
        super().__init__(name, ServerProvider.VANILLA)
        self._manifest = manifest

    def _get_url(self) -> str:
        version_data = requests.get(self._manifest["url"]).json()
        return version_data["downloads"]["server"]["url"]


class PaperVersion(ServerVersion):
    def __init__(self, name: str):
        super().__init__(name, ServerProvider.PAPERMC)

    def _get_url(self) -> str:
        version_data = requests.get(f"{PAPER_BASE_URL}/{self.name}").json()
        return f"{PAPER_BASE_URL}/{self.name}/{version_data['builds']['latest']}/download"


def confirm(msg: str, default: bool = False) -> bool:
    """
    Ask the user to confirm an action.

    Usage:
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

    Usage:
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
