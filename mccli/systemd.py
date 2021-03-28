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
    def __init__(self, name: str, bus: BusType = BusType.SYSTEM):
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
        self._unit_path = self._manager.LoadUnit(self.name)
        self._unit = self._bus.get_object(
            "org.freedesktop.systemd1",
            self._unit_path
        )
        self._unit_props = dbus.Interface(
            self._unit, "org.freedesktop.DBus.Properties")

    def start(self):
        """
        Start a service
        """
        self._manager.StartUnit(self.name, "replace")

    def stop(self):
        """
        Stops a service
        """
        self._manager.StopUnit(self.name, "replace")

    def restart(self):
        """
        Restarts a service
        """
        self._manager.RestartUnit(self.name, "replace")

    def enable(self, now: bool = False):
        """
        Enables a service, and starts it if now=True
        """
        self._manager.EnableUnitFiles([self.name], False, False)
        if now:
            self.start()

    def disable(self, now: bool = False):
        """
        Disables a service, and stops it if now=True
        """
        self._manager.DisableUnitFiles([self.name], False)
        if now:
            self.stop()

    def reload(self):
        self._manager.ReloadUnit(self.name, "replace")

    @property
    def status(self) -> SystemdActiveState:
        return SystemdActiveState(self._unit_props.Get('org.freedesktop.systemd1.Unit', 'ActiveState'))

    @property
    def sub_state(self) -> str:
        return self._unit_props.Get("org.freedesktop.systemd1.Unit", "SubState")

    @property
    def enablement(self) -> SystemdEnablementState:
        return SystemdEnablementState(
            self._manager.GetUnitFileState(self.name)
        )

    @property
    def description(self) -> str:
        return str(self._unit_props.Get("org.freedesktop.systemd1.Unit", "Description"))


class Service(Unit):
    pass
