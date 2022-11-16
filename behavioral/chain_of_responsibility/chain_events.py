class Event:
    def __init__(self):
        self._accepted = None

    def __str__(self):
        return type(self).__name__.replace('Event', '').lower()

    @property
    def accepted(self):
        return self._accepted

    @accepted.setter
    def accepted(self, value):
        self._accepted = value


class MouseClickEvent(Event):
    def __init__(self, x, y, button):
        super().__init__()
        self.x = x
        self.y = y
        self.button = button


class KeyPressedEvent(Event):
    def __init__(self, key_code, modifiers):
        super().__init__()
        self.key_code = key_code
        self.modifiers = modifiers


class PaintEvent(Event):
    def __init__(self):
        super().__init__()


class CloseEvent(Event):
    def __init__(self):
        super().__init__()


class Widget:
    def __init__(self, parent=None):
        self.parent = parent
        self.widgets = []

    def add_widget(self, child_widget):
        self.widgets.append(child_widget)
        child_widget.parent = self

    def handle(self, event):
        # dispatching events
        handler = 'handle_{}'.format(event)

        if hasattr(self, handler):
            method = getattr(self, handler)
            method(event)
        elif hasattr(self, 'handle_default'):
            self.handle_default(event)

        # forwarding an event to all children
        for child in self.widgets:
            if not event.accepted:
                child.handle(event)


class MainWindow(Widget):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def handle_close(self, _):
        print('Closing {}...'.format(self.name))

    def handle_default(self, event):
        print('MainWindow: {} - default handler: {}'.format(self.name, event))


class Dialog(Widget):
    def __init__(self, parent, name):
        super().__init__(parent)
        self.name = name

    def handle_paint(self, event):
        print('Dialog {} is repainted...'.format(self.name))


class TextBox(Widget):
    def __init__(self, parent, name):
        super().__init__(parent)
        self.name = name
        self.text = ''

    def handle_keypressed(self, event):
        char = chr(event.key_code)
        print('TextBox {} handles keypressed event - {}'.format(self.name, char))


class Button(Widget):
    def __init__(self, parent, name):
        super().__init__(parent)
        self.name = name

    def handle_mouseclick(self, event):
        print('Button handles mouse clicked at ({}, {})'.format(event.x, event.y))

    def handle_paint(self, _):
        print('Button {} is repainted...'.format(self.name))


if __name__ == '__main__':
    # building a window
    wnd = MainWindow("App")
    dlg = Dialog(wnd, 'Input text')

    txt_box = TextBox(dlg, 'Name')
    btn_ok = Button(dlg, 'Ok')
    dlg.add_widget(txt_box)
    dlg.add_widget(btn_ok)
    wnd.add_widget(dlg)

    # raising events
    events = [MouseClickEvent(1, 2, 'left'), PaintEvent(), KeyPressedEvent(65, 'Shift'), MouseClickEvent(54, 23, 'right'),
              KeyPressedEvent(65, 'Shift'), CloseEvent()]

    for event in events:
        print('Event {} is raised...'.format(str(event)))
        wnd.handle(event)
        print('-'*40)
