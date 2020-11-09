from .config_parser import dump, load
from .systemd import Service
from .online_utils import ServerVersion, ServerProvider, get_version
from .utils import OPTIONS, SERVER_BASE_PATH
import pathlib


class Server:
    def __init__(self, name: str, version: ServerVersion = None):
        # super().__init__(OPTIONS["service_template_name"].format(name=name))
        self.name = name
        self._version = None
        if version:
            self.version = version

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
    def version(self):
        if not self._version:
            try:
                with self.path.joinpath(OPTIONS["paths"]["server_dat"]).open() as file:
                    data = load(file)
                    self._version = get_version(
                        data["name"], ServerProvider(data["provider"]))
            except FileNotFoundError:
                
                return None
        return self._version

    @version.setter
    def version(self, version: ServerVersion):
        
        self.path.mkdir(exist_ok=True)
        if not self.version or not (self._version.provider == version.provider and self.version.name == version.name):
            with self.path.joinpath(OPTIONS["paths"]["server_dat"]).open("w") as file:
                dump({"name": version.name, "provider": version.provider.value}, file)

            with self.path.joinpath(OPTIONS["paths"]["server_jar"]).open("wb") as file:
                file.write(version.download())
        
        self._version = version
