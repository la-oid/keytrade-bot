from .inline import MenuKeyboards, MarketKeyboards, ProfileKeyboards
from .reply import MenuReplyKeyboards


class InlineKeyboards:
    def __init__(self):
        self.menu = MenuKeyboards()
        self.market = MarketKeyboards()
        self.profile = ProfileKeyboards()


class ReplyKeyboards:
    def __init__(self):
        self.menu = MenuReplyKeyboards()


__all__ = ["InlineKeyboards", "ReplyKeyboards"]