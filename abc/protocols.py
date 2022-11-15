import dataclasses
from typing import Protocol, Union


@dataclasses.dataclass
class SystemManager:
    name: str

    def run(self) -> None:
        print(f"{self.name} is running...")


class Printable(Protocol):
    def print(self, msg: str) -> None: ...


class UberDeviceManager(Protocol):
    def add_device(self, device): ...
    def get_system_manager(self) -> SystemManager: ...


class MyUDM:
    def add_device(self, device):
        print(f"add device {device}")

    def get_system_manager(self):
        return SystemManager("System Manager")

    def print(self, msg: str) -> None:
        print(msg)


def client(manager: Union[UberDeviceManager, Printable]):
    manager.add_device("server")
    sys_manager = manager.get_system_manager()

