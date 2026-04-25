from .inline import MenuKeyboards, VerifyKeyboards


class InlineKeyboards:
    def __init__(self):
        self.menu = MenuKeyboards()
        self.verify = VerifyKeyboards()


__all__ = ["InlineKeyboards"]