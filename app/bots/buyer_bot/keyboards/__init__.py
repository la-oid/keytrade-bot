from .inline import MenuKeyboards, MiscKeyboards, WholesaleKeyboards


class InlineKeyboards:
    def __init__(self):
        self.menu = MenuKeyboards()
        self.misc = MiscKeyboards()
        self.wholesale = WholesaleKeyboards()


__all__ = ["InlineKeyboards"]
