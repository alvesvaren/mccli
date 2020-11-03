
from enum import Enum
from typing import Union
import dbus


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


class SystemdEnablementState(Enum):
    ENABLED = "enabled"
    ENABLED_RUNTIME = "enabled-runtime"
    LINKED = "linked"
    LINKED_RUNTIME = "linked-runtime"
    ALIAS = "alias"
    MASKED = "masked"
    MASKED_RUNTIME = "masked-runtime"
    STATIC = "static"
    INDIRECT = "indirect"
    DISABLED = "disabled"
    GENERATED = "generated"
    TRANSIENT = "transient"
    BAD = "bad"


class SystemdStatusState(Enum):
    OK = 0
    DEAD_PID = 1
    DEAD_LOCK = 2
    DEAD = 3
    UNKNOWN = 4


class BusType(Enum):
    SYSTEM = 0
    SESSION = 1


class Unit:
    def __init__(self, name: str, bus: BusType):
        if not name.endswith((
            ".service", ".target",
            ".socket", ".device", ".mount",
            ".automount", ".swap", ".path",
            ".timer", ".snapshot", ".scope"
        )):
            name += ".service"
        self.name = name
        self._bus = dbus.SystemBus() \
            if bus == BusType.SYSTEM \
            else dbus.SessionBus()
        self._systemd = self._bus.get_object(
            'org.freedesktop.systemd1',
            '/org/freedesktop/systemd1'
        )
        self._manager = dbus.Interface(
            self._systemd,
            'org.freedesktop.systemd1.Manager'
        )

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

    def reload(self):
        raise NotImplementedError

    @property
    def status(self) -> SystemdStatusState:
        raise NotImplementedError

    @property
    def enabled(self) -> SystemdEnablementState:
        return SystemdEnablementState(
            self._manager.GetUnitFileState(self.name)
        )


class Service(Unit):
    pass
