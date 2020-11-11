from .runner import run_jar, run_tmux
from .tmux_utils import get_pane, get_session, get_sessions_matching
from .config_parser import dump, load
from typing import List, Union
from .server_utils import Server
from .online_utils import ServerProvider, ServerVersion, find_version, get_versions
from .utils import choice, confirm, OPTIONS, custom_choice, SERVER_BASE_PATH
import mccli
import os

os.chdir(SERVER_BASE_PATH)
VERBOSE: bool = OPTIONS["verbose_output"]


def select_version(provider: ServerProvider = None, *, verbose: bool = VERBOSE) -> mccli.ServerVersion:
    """
    Allow the user to select version
    """
    if not provider:
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
    raise ValueError("Did not select a valid version")


def create(name: str = None, provider: ServerProvider = None, *, verbose: bool = VERBOSE) -> Server:
    if not name:
        name = custom_choice("What should the server be called?")

    version = select_version(provider)
    if verbose:
        print(f"Downloading server.jar from {version.url}...", end="")
    server = Server(name, version)
    if verbose:
        print("DONE!")
    if confirm("Do you accept the Minecraft EULA (read at https://www.minecraft.net/eula)?"):
        with server.path.joinpath("eula.txt").open("w") as file:
            file.write("eula=true\n")
            if verbose:
                print("Accepted eula.")
    return server


def update(name: str, version: ServerVersion = None, *, verbose: bool = VERBOSE):
    if not version:
        version = select_version()

    server = Server(name)

    if verbose:
        print("Replacing server.jar with new version")

    server.version = version


def modify(name: str, key: str, value: Union[str, int, float, bool], file_name: str = "server.properties", *, verbose: bool = VERBOSE):
    server = Server(name)
    absolute_path = server.path.joinpath(file_name)
    with absolute_path.open() as file:
        old_data = load(file)
        new_data = old_data
    try:
        new_data[key] = value
        with absolute_path.open("w") as file:
            dump(new_data, file)
        print(f"Wrote '{key}={value}' to {file_name}")
    except Exception as error:
        # Try recovering from error and writing back the old data
        with absolute_path.open("w") as file:
            dump(old_data, file)
        raise error


def runner(name: str, in_tmux: bool = False, *, verbose: bool = VERBOSE):
    code = 0
    if in_tmux:
        code = run_tmux(name)
    else:
        code = run_jar(name)
    exit(code)


def run(name: str, command: Union[List[str], str], *, verbose: bool = VERBOSE):
    if type(command) != str:
        command = " ".join(command)
    print(f"Running '{command}' in mc-{name}")
    Server(name).run_command(command)
    exit(0)
    # exit(os.system(f"/usr/bin/tmux send-keys -t mc-{name} '{command}' ENTER"))


def attach(name: str, *, verbose: bool = VERBOSE):
    print(f"Attach to console of server named {name}")
    get_session("mc-"+name).attach_session()
    # exit(os.system(f"/usr/bin/tmux attach -t mc-{name}"))


def list_command(*, verbose: bool = VERBOSE):
    sessions = get_sessions_matching("mc-")
    session_names = [i.get("session_name")[3:] for i in sessions]
    print("Currently running servers:")
    for name in session_names:
        server = Server(name)
        print(f"  - {server.name} : {server.version}")
    # print(session_names)
