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


class ShapeGroup(Shape):
    def __init__(self):
        self._shapes: List[Shape] = []

    def move(self, dx, dy):
        [s.move(dx, dy) for s in self._shapes]

    def draw(self):
        for s in self._shapes:
            s.draw()

    def add(self, shp: Shape):
        self._shapes.append(shp)

    def remove(self, shp: Shape):
        self._shapes.remove(shp)

    def __iter__(self):
        for s in self._shapes:
            yield s


if __name__ == "__main__":
    c = Circle(10, 20, 200)
    c.draw()
    c.move(100, 500)
    c.draw()

    assert isinstance(c, Shape)
    assert issubclass(Circle, Shape)

    r = Rectangle(10, 200, 500, 100)    
    r.draw()

    shapes = ShapeGroup()
    shapes.add(c)
    shapes.add(r)
    shapes.add(Rectangle(100, 200, 200, 500))

    print('*' * 60)

    shapes.draw()

    print('*' * 60)

    shapes.move(30, 70)
    shapes.draw()

    for s in shapes:
        print(s)