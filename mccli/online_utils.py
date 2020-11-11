from typing import List, Dict, Union
import requests
from enum import Enum
from . import utils

URLS: Dict[str, str] = utils.OPTIONS["urls"]
PAPER_BASE_URL = URLS["papermc"].rstrip("/")


class ServerProvider(Enum):
    """
    Represents a server provider like vanilla or papermc for a server version
    """
    VANILLA = "vanilla"
    PAPERMC = "papermc"
    SPIGOT = "spigot"


class VanillaVersionType(Enum):
    SNAPSHOT = "snapshot"
    RELEASE = "release"
    OLD_ALPHA = "old_alpha"
    OLD_BETA = "old_beta"


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
        self.version_type: VanillaVersionType = VanillaVersionType(
            manifest["type"])

    def _get_url(self) -> str:
        version_data = requests.get(self._manifest["url"]).json()
        return version_data["downloads"]["server"]["url"]


class PaperVersion(ServerVersion):
    def __init__(self, name: str):
        super().__init__(name, ServerProvider.PAPERMC)

    def _get_url(self) -> str:
        version_data = requests.get(f"{PAPER_BASE_URL}/{self.name}").json()
        return f"{PAPER_BASE_URL}/{self.name}/{version_data['builds']['latest']}/download"


def get_vanilla_versions(*, releases: bool = True, snapshots: bool = False, old_versions: bool = False, all_versions: bool = False) -> List[ServerVersion]:
    """
    Get a list of server versions avalible for download from the vanilla provider matching the arguments, defaults to all official full releases.

    ```py
    versions = mccli.get_vanilla_versions(snapshots=True)
    latest_version = versions[0]
    ```
    """
    versions: List[ServerVersion] = []
    manifest = requests.get(URLS["vanilla"]).json()

    for version in manifest["versions"]:
        version_type = VanillaVersionType(version["type"])
        if not all_versions:
            if (not snapshots and version_type == VanillaVersionType.SNAPSHOT):
                continue
            if not releases and version_type == VanillaVersionType.RELEASE:
                continue
            if not old_versions and version_type in (VanillaVersionType.OLD_ALPHA, VanillaVersionType.OLD_BETA):
                continue
        versions.append(VanillaVersion(
            version["id"], version))
    return versions


def get_paper_versions() -> List[ServerVersion]:
    """
    Get a list of server versions avalible for download from the paper provider

    ```py
    versions = mccli.get_paper_versions()
    latest_version = versions[0]
    ```
    """
    versions: List[ServerVersion] = []

    provided_versions = requests.get(PAPER_BASE_URL).json()
    for version in provided_versions["versions"]:
        versions.append(PaperVersion(version))

    return versions


def get_versions(provider: ServerProvider) -> List[ServerVersion]:
    """
    Get a list of server versions from the provided provider

    ```py
    versions = mccli.get_versions(mccli.ServerProvider.PAPER)
    latest_version = versions[0]
    ```
    """

    if provider == ServerProvider.VANILLA:
        return get_vanilla_versions()

    elif provider == ServerProvider.PAPERMC:
        return get_paper_versions()

    elif provider == ServerProvider.SPIGOT:
        raise NotImplementedError("Spigot support is not implemented")


def find_version(name: str, versions: List[ServerVersion]) -> Union[ServerVersion, None]:
    selected_version = None
    for version in versions:
        if version.name == name:
            selected_version = version
            break
    return selected_version


def get_version(name: str, provider: ServerProvider):
    versions = get_versions(provider)
    return find_version(name, versions)
