from typing import Protocol


class Shape(Protocol):
    def draw(self): ...


class ShapeFactory:
    creators = {}

    @classmethod
    def make_shape(cls, id):
        try:
            retval = cls.creators[id]
        except KeyError as err:
            raise NotImplementedError(f"{id=} doesn't exist") from err
        return retval()

    @classmethod
    def register(cls, type_name):
        def deco(deco_cls):
            cls.creators[type_name] = deco_cls
            return deco_cls
        return deco


@ShapeFactory.register('Rectangle')
class Rectangle:
    def draw(self):
        print("Rect")


@ShapeFactory.register('Square')
class Square:
    def draw(self):
        print("Square!!!")


if __name__ == "__main__":
    shp = ShapeFactory.make_shape("Square")
    shp.draw()
