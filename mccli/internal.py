from .utils import *


def get_vanilla_versions(*, releases: bool = True, snapshots: bool = False) -> List[ServerProvider]:
    """
    Get a list of server versions avalible for download from the vanilla provider
    Usage:
    ```py
    versions = mccli.get_vanilla_versions(snapshots=True)
    latest_version = versions[0]
    ```
    """
    versions: List[ServerVersion] = []
    manifest = requests.get(URLS["vanilla"]).json()

    for version in manifest["versions"]:
        if not snapshots and version["type"] == ServerType.SNAPSHOT.value:
            continue
        if not releases and version["type"] == ServerType.RELEASE.value:
            continue
        versions.append(VanillaVersion(
            version["id"], version))
    return versions


def get_paper_versions() -> List[ServerProvider]:
    """
    Get a list of server versions avalible for download from the paper provider
    Usage:
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

    if provider == ServerProvider.VANILLA:
        return get_vanilla_versions()

    elif provider == ServerProvider.PAPERMC:
        return get_paper_versions()

    elif provider == ServerProvider.SPIGOT:
        raise NotImplementedError("Spigot support is not implemented")