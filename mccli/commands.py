from .server_utils import Server
from . import config_parser
from .online_utils import find_version, get_versions
from .utils import choice, confirm, OPTIONS, custom_choice, SERVER_BASE_PATH
import mccli
import os
from pathlib import Path

os.chdir(SERVER_BASE_PATH)

def select_version(*, verbose: bool = True) -> mccli.ServerVersion:
    """
    Allow the user to select version
    """

    providers = ["vanilla", "papermc"]
    provider = mccli.ServerProvider(
        providers[choice("Select provider", providers)])
    if verbose:
        print("\nSelected", provider.value, "provider.")
        print("Fetching versions from provider...", end="")
    versions = mccli.get_versions(provider)
    if verbose:
        print("DONE!")
    version_name = custom_choice(
        f"Select version from {provider.value} provider", versions[0].name)
    selected_version = find_version(version_name, versions)
    if not selected_version and provider == mccli.ServerProvider.VANILLA:
        versions = mccli.get_vanilla_versions(all_versions=True)
        selected_version = find_version(version_name, versions)
    if selected_version:
        if verbose:
            print("Selected version", selected_version.name)
        return selected_version
    return None


def create(name: str = None, *, verbose: bool = True) -> Server:
    if not name:
        name = custom_choice("What should the server be called?")

    server_dir = SERVER_BASE_PATH.joinpath(name)
    version = select_version()
    if not version:
        raise ValueError("Did not select a valid version")
    server = Server(name, version)
    if verbose:
        print(f"Downloading server.jar from {version.url}...", end="")
    print("DONE!")
    if confirm("Do you accept the Minecraft EULA (read at https://www.minecraft.net/eula)?"):
        with server_dir.joinpath("eula.txt").open("w") as file:
            file.write("eula=true\n")
            if verbose:
                print("Accepted eula.")
    return server