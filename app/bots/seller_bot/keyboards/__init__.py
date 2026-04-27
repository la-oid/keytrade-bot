from .inline import MenuKeyboards, MiscKeyboards
from .reply import MenuReplyKeyboards


class InlineKeyboards:
    def __init__(self):
        self.menu = MenuKeyboards()
        self.misc = MiscKeyboards()


class ReplyKeyboards:
    def __init__(self):
        self.menu = MenuReplyKeyboards()


__all__ = ["InlineKeyboards", "ReplyKeyboards"]