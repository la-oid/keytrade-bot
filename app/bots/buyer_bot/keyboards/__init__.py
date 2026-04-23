from .inline import MenuKeyboards, MiscKeyboards


class InlineKeyboards:
    def __init__(self):
        self.menu = MenuKeyboards()
        self.misc = MiscKeyboards()


__all__ = ["InlineKeyboards"]