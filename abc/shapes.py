import abc
from collections import namedtuple
from typing import List
from dataclasses import dataclass


@dataclass
class Coord:
    x: int
    y: int

    def translate(self, dx, dy):
        self.x += dx
        self.y += dy


class Shape:
    """Refactor Shape class to ABC
    """

    def __init__(self, x, y, ):
        self.__coord = Coord(x, y)

    @property
    def coordinates(self) -> Coord:
        return self.__coord

    def move(self, dx, dy) -> None:
        self.__coord.translate(dx, dy)

    def draw(self):
        pass


class Circle(Shape):
    def __init__(self, x, y, r):
        super().__init__(x, y)
        self.__radius = r

    def draw(self) -> None:
        print(f'Circle at {self.coordinates} with radius {self.__radius}')


class Rectangle(Shape):
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


def draw_shapes(shapes: List[Shape]):
    shapes.draw()


if __name__ == "__main__":
    c = Circle(10, 20, 200)
    c.draw()
    c.move(100, 500)
    c.draw()

    assert isinstance(c, Shape)
    assert issubclass(Circle, Shape)

    r = Rectangle(10, 200, 500, 100)
    r.draw()
