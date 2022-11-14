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


class Square:
    def __init__(self, size):
        self.__rect_impl = Rectangle(size, size)

    @property
    def size(self):
        assert self.__rect_impl.width == self.__rect_impl.height
        return self.__rect_impl.height

    @size.setter
    def size(self, w):
        self.__rect_impl.width = w
        self.__rect_impl.height = w

    def draw(self):
        self.__rect_impl.draw()


def calc_area(rect: Rectangle):
    return rect.width * rect.height


if __name__ == "__main__":
    rect = Square(100)
    rect.draw()

    # rect.width = 10
    # rect.height = 20
    # assert calc_area(rect) == 200
