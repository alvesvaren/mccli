from .utils import *


def get_vanilla_versions(*, releases: bool = True, snapshots: bool = False) -> List[ServerProvider]:
    versions: List[ServerVersion] = []

    manifest = requests.get(URLS["vanilla"]).json()
    manifest_versions: List[dict] = manifest["versions"]
    
    for version in manifest["versions"]:
        if not snapshots and version["type"] == ServerType.SNAPSHOT.value:
            continue
        if not releases and version["type"] == ServerType.RELEASE.value:
            continue
        versions.append(VanillaVersion(
            version["id"], version))
    return versions


def get_paper_versions() -> List[ServerProvider]:
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