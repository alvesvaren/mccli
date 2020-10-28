import requests
import json
from .utils import *

with open("options.json") as file:
    OPTIONS = json.load(file)
    URLS = OPTIONS["urls"]


def get_vanilla_versions() -> List[ServerProvider]:
    versions: List[ServerVersion] = []

    manifest = requests.get(URLS["vanilla"]).json()
    for version in manifest["versions"]:
        version_data = requests.get(version["url"]).json()
        url = version_data["downloads"]["server"]
        versions.append(ServerVersion(
            version["id"], url, ServerProvider.VANILLA))
    return versions


def get_paper_versions(all_builds: bool = False) -> List[ServerProvider]:
    versions: List[ServerVersion] = []

    base_url: str = URLS["papermc"].rstrip("/")
    provided_versions = requests.get(base_url).json()
    for version in provided_versions["versions"]:
        version_data = requests.get(base_url + "/" + version)
        if all_builds:
            for build in version_data["builds"]["all"]:
                versions.append(ServerVersion(
                    version + "-" + build,
                    f"{base_url}/{version}/{build}/download",
                    ServerProvider.PAPERMC))


def get_versions(provider: ServerProvider) -> List[ServerVersion]:

    if provider == ServerProvider.VANILLA:
        return get_vanilla_versions()

    elif provider == ServerProvider.PAPERMC:
        return get_paper_versions()

    elif provider == ServerProvider.SPIGOT:
        raise NotImplementedError("Spigot support is not implemented")
