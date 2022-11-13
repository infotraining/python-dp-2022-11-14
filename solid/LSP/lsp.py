class Rectangle:
    def __init__(self, width, height):
        self._width = width
        self._height = height

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, w):
        self._width = w

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, h):
        self._height = h

    def draw(self):
        print(f"Rectangle({self.width}, {self.height})")


class Square(Rectangle):
    def __init__(self, size):
        super().__init__(size, size)

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, w):
        self._width = w
        self._height = w

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, h):
        self._height = h
        self._width = h


def calc_area(rect: Rectangle):
    return rect.width * rect.height


if __name__ == "__main__":
    rect = Rectangle(100, 200)
    rect.draw()

    rect.width = 10
    rect.height = 20
    assert calc_area(rect) == 200
