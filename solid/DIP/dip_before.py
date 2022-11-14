from collections import namedtuple
from dataclasses import dataclass
from typing import Protocol


RGB = namedtuple('RGB', ['R', 'G', 'B'])


class ISwitch(Protocol):
    def on(self): ...

    def off(self): ...


@dataclass
class LEDLight:
    color: RGB

    def set_rgb(self, color: RGB):
        self.color = color
        print(f'Color({color.R}, {color.G}, {color.B}) is set for a LED light')


class ToggleButton:
    def __init__(self, switch: ISwitch) -> None:
        self._is_on = False
        self.__switch_impl = switch

    def click(self):
        if self._is_on:
            self._is_on = False
            self.__switch_impl.off()
        else:
            self._is_on = True
            self.__switch_impl.on()

class LedAdapter(LEDLight):
    def on(self):
        self.set_rgb(RGB(255, 255, 255))
        
    def off(self):
        self.set_rgb(RGB(0, 0, 0))

class LedSwitch:
    """"Object adapter"""

    def __init__(self, led_light = None):
        self.led_light = led_light or LEDLight(RGB(0, 0, 0))

    def on(self):
        self.led_light.set_rgb(RGB(255, 255, 255))

    def off(self):
        self.led_light.set_rgb(RGB(0, 0, 0))


if __name__ == "__main__":
    btn = ToggleButton(LedSwitch())
    btn.click()
    btn.click()
    btn.click()
    btn.click()
