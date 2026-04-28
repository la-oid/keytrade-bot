from .inline import MenuKeyboards, MarketKeyboards
from .reply import MenuReplyKeyboards


class InlineKeyboards:
    def __init__(self):
        self.menu = MenuKeyboards()
        self.market = MarketKeyboards()


class ReplyKeyboards:
    def __init__(self):
        self.menu = MenuReplyKeyboards()


__all__ = ["InlineKeyboards", "ReplyKeyboards"]