from .systemd import Service
from .online_utils import ServerVersion, ServerProvider
from .utils import SERVER_BASE_PATH
import pathlib


class Server(Service):
    def __init__(self, name: str, version: ServerVersion):
        self.name = name
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
