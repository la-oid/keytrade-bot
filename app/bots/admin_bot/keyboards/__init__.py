from .inline import MenuKeyboards


class InlineKeyboards:
    def __init__(self):
        self.menu = MenuKeyboards()


__all__ = ["InlineKeyboards"]