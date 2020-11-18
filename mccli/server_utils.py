from mccli.tmux_utils import get_pane, get_session
from typing import List
from .config_parser import dump, load, LoadDict
from .systemd import BusType, Service
from .online_utils import ServerVersion, ServerProvider, get_version
from .utils import OPTIONS, SERVER_BASE_PATH
import pathlib
import os

SERVER_DAT_PATH = OPTIONS["paths"]["server_dat"]


class Server:
    def __init__(self, name: str):
        # super().__init__(OPTIONS["service_template_name"].format(name=name))
        self.name = name
        self._version = None

    @property
    def _dat_file_content(self):
        try:
            with self.path.joinpath(SERVER_DAT_PATH).open() as file:
                return load(file)
        except FileNotFoundError:
            return {}

    @_dat_file_content.setter
    def _dat_file_content(self, new_content: LoadDict):
        new_data = {**self._dat_file_content, **new_content}
        with self.path.joinpath(SERVER_DAT_PATH).open("w") as file:
            dump(new_data, file)

    @property
    def provider(self) -> ServerProvider:
        return self.version.provider

    @property
    def path(self) -> pathlib.Path:
        path = SERVER_BASE_PATH.joinpath(self.name)
        path.mkdir(exist_ok=True)

        return path

    def run_command(self, command: str):
        """
        Runs a command in the server console (only for tmux runners)
        """
        get_pane(get_session("mc-"+self.name)).send_keys(command)

    @property
    def args(self) -> List[str]:
        try:
            return self._dat_file_content["args"].split(" ")
        except (FileNotFoundError, KeyError):
            return []

    @args.setter
    def args(self, value: List[str]):
        self._dat_file_content = {"args": " ".join(value)}

    @property
    def version(self):
        if not self._version:
            try:
                data = self._dat_file_content
                self._version = get_version(
                    data["name"], ServerProvider(data["provider"]))
            except KeyError:
                return None

        return self._version

    def update(self, version: ServerVersion):

        self._dat_file_content = {
            "name": version.name, "provider": version.provider.value}

        with self.path.joinpath(OPTIONS["paths"]["server_jar"]).open("wb") as file:
            file.write(version.download())


def get_server_service(name: str):
    if not "XDG_RUNTIME_DIR" in os.environ:
        os.environ["XDG_RUNTIME_DIR"] = OPTIONS["paths"]["xdg_runtime_dir"].format(os.getuid())
    return Service(f"minecraft-server@{name}.service", BusType.SESSION)
