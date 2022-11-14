from io import StringIO
from typing import Dict, Union


class Shape:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Circle(Shape):
    def __init__(self, x, y, r):
        super().__init__(x, y)
        self.r = r

    def draw(self):
        print('Circle x={} y={} r={}'.format(self.x, self.y, self.r))


class Rectangle(Shape):
    def __init__(self, x, y, w, h):
        super().__init__(x, y)
        self.w = w
        self.h = h

    def draw(self):
        print('Rectangle x={} y={} w={} h={}'.format(self.x, self.y, self.w, self.h))

class Square(Rectangle):
    def __init__(self, x, y, a):
        super().__init__(x, y, a, a)

    def draw(self):
        print('Square x={} y={} w={} h={}'.format(self.x, self.y, self.w, self.h))


shapes_factory: Dict[str, Union[Circle, Rectangle]] = {
    "Square": lambda x, y, a: Rectangle(x, y, a, a),
    "Rectangle": Rectangle,
    "Circle": Circle
}


mapper = {
    'Circle': Circle,
    'Rectangle': Rectangle,
    'Square': Square
}


class Drawing:
    def __init__(self, shapes):
        self._shapes = shapes

    def __repr__(self):
        return '<Drawing {}>'.format(str(self._shapes))

    @classmethod
    def from_stream(cls, stream):
        shapes = []
        for line in stream:
            line = line.strip()
            if not line:
                continue
            shape_name, *parameters = line.split()
            parameters = map(int, parameters)
            try:
                shape = mapper[shape_name](*parameters)
                shapes.append(shape)
            except KeyError:
                print(f"No shape named '{shape_name}' found.")
        return cls(shapes)



if __name__ == "__main__":
    
    raw_shapes = '''
Circle 15 10 14
Rectangle 30 30 100 150
Circle 40 20 5
Square 30 100 20
Ziemniaczek 10 10 10 10
'''

    graphics = Drawing.from_stream(StringIO(raw_shapes))
    graphics.render()
