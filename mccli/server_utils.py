from typing import List
from .config_parser import dump, load, LoadDict
from .systemd import BusType, Service
from .online_utils import ServerVersion, ServerProvider, get_version
from .utils import OPTIONS, SERVER_BASE_PATH
import pathlib

SERVER_DAT_PATH = OPTIONS["paths"]["server_dat"]

class Server:
    def __init__(self, name: str, version: ServerVersion = None):
        # super().__init__(OPTIONS["service_template_name"].format(name=name))
        self.name = name
        self._version = version

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
        return SERVER_BASE_PATH.joinpath(self.name)

    def run_command(self, command: str):
        """
        Runs a command in the server console
        """
        raise NotImplementedError
    
    @property
    def args(self) -> List[str]:
        try:
            return self._dat_file_content["args"].split(" ")
        except (FileNotFoundError, KeyError):
            return []
    
    @args.setter
    def args(self, value: List[str]):
        self._dat_file_content = {"args" : " ".join(value)}

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

    @version.setter
    def version(self, version: ServerVersion):

        self.path.mkdir(exist_ok=True)
        self._dat_file_content = {"name": version.name, "provider": version.provider.value}

        with self.path.joinpath(OPTIONS["paths"]["server_jar"]).open("wb") as file:
            file.write(version.download())

        self._version = version


def get_server_service(name: str):
    return Service(f"minecraft-server@{name}.service", BusType.SYSTEM)
