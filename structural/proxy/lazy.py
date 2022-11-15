
import time

class LazyProperty:
    def __init__(self, method):
        self.method = method
        self.method_name = method.__name__
        print('function overridden: {}'.format(self.method))
        print("function's name: {}".format(self.method_name))

    def __get__(self, obj, cls):
        if not obj:
            return None
        value = self.method(obj)
        setattr(obj, self.method_name, value)
        return value


class Image:
    def __init__(self, x, y, path):
        self.coordinates = (x, y)
        self._path = path
        self._bitmap = None

    @LazyProperty
    def bitmap(self):
        print(f'Initializing self._bitmap ', end="")
        for _ in range(10):
            time.sleep(1)
            print('.', end="", flush=True)
        
        self._bitmap = [c for c in f"Bitmap({self._path})"]
        print(f'\nBitmap loaded: {self._bitmap} ')
        return self._bitmap


def main():
    print('-' * 40)

    img = Image(10, 20, "test.png")

    print(f"Image coordinates: {img.coordinates}")
    print(f"Image bitmap: {img.bitmap}")

    img.coordinates = (40, 20)
    print('-' * 40)

    print(f"Image coordinates: {img.coordinates}")
    print(f"Image bitmap: {img.bitmap}")


if __name__ == '__main__':
    main()
