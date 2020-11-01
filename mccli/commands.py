from mccli.online_utils import find_version, get_versions
from .utils import choice, confirm, OPTIONS, custom_choice
import mccli


def select_version(verbose: bool = True) -> mccli.ServerVersion:
    """
    Allow the user to select version
    """

    providers = ["vanilla", "papermc"]
    provider = mccli.ServerProvider(
        providers[choice("Select provider", providers)])
    if verbose: 
        print()
        print("Selected", provider.value, "provider.")
        print("Fetching versions from provider...")
        print()
    versions = mccli.get_versions(provider)
    version_name = custom_choice(f"Select version from {provider.value} provider", versions[0].name)
    selected_version = find_version(version_name, versions)
    if not selected_version and provider == mccli.ServerProvider.VANILLA:
        versions = mccli.get_vanilla_versions(all_versions=True)
        selected_version = find_version(version_name, versions)
    if selected_version:
        if verbose:
            print("Selected version", selected_version.name)
        return selected_version
    return None