import abc
from collections import namedtuple
from typing import List, Protocol, Union
from dataclasses import dataclass


@dataclass
class Coord:
    x: int
    y: int

    def translate(self, dx, dy):
        self.x += dx
        self.y += dy


class Shape(abc.ABC):
    @abc.abstractmethod
    def move(self, dx, dy) -> None:
        pass

    @abc.abstractmethod
    def draw(self) -> None:
        pass

    @property
    @abc.abstractmethod
    def coordinates(self) -> Coord:
        pass


class ShapeBase(Shape):
    """Refactor Shape class to ABC
    """

    def __init__(self, x, y, ):
        self.__coord = Coord(x, y)

    @property
    def coordinates(self) -> Coord:
        return self.__coord

    @abc.abstractmethod
    def move(self, dx, dy) -> None:
        self.__coord.translate(dx, dy)


class Circle(ShapeBase):
    def __init__(self, x, y, r):
        super().__init__(x, y)
        self.__radius = r

    def move(self, dx, dy):
        super().move(dx, dy)

    def draw(self) -> None:
        print(f'Circle at {self.coordinates} with radius {self.__radius}')


class Rectangle(ShapeBase):
    def __init__(self, x, y, w, h):
        super().__init__(x, y)
        self.__width = w
        self.__height = h

    @property
    def width(self):
        return self.__width

    @width.setter
    def width(self, new_width):
        self.__width = new_width

    @property
    def height(self):
        return self.__height

    @height.setter
    def height(self, new_height):
        self.__height = new_height

    def draw(self) -> None:
        print(
            f'Rectangle at {self.coordinates} with width={self.__width} & height={self.__height}')

    def move(self, dx, dy):
        super().move(dx, dy)


# def draw_shapes(shapes: List[Shape]):
#     shapes.draw()

@dataclass
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


if __name__ == "__main__":
    c = Circle(10, 20, 200)
    c.draw()
    c.move(100, 500)
    c.draw()

    assert isinstance(c, Shape)
    assert issubclass(Circle, Shape)

    r = Rectangle(10, 200, 500, 100)    
    r.draw()

device_manager = MyUDM()
client(device_manager)
