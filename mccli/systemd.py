
from enum import Enum
from typing import Union


class SystemdActiveState(Enum):
    ACTIVE = "active"
    RELOADING = "reloading"
    FAILED = "failed"
    INACTIVE = "inactive"
    ACTIVATING = "activating"
    DEACTIVATING = "deactivating"


class SystemdLoadState(Enum):
    LOADED = "loaded"
    NOT_FOUND = "not-found"
    BAD_SETTING = "bad-setting"
    ERROR = "error"
    MASKED = "masked"


class SystemdStatusState(Enum):
    OK = 0
    DEAD_PID = 1
    DEAD_LOCK = 2
    DEAD = 3
    UNKNOWN = 4


class Unit:
    def __init__(self, name: str):
        self.name = name

    def start(self) -> int:
        """
        Start a server, returns exit status if failed, else 0
        """
        raise NotImplementedError

    def stop(self):
        raise NotImplementedError

    def restart(self) -> int:
        raise NotImplementedError

    def enable(self, now: bool = False) -> Union[int, None]:
        """
        Retruns exit code from start if called with now
        """
        raise NotImplementedError

    def disable(self, now: bool = False):
        raise NotImplementedError

    def status(self):
        raise NotImplementedError


class Service(Unit):
    pass
