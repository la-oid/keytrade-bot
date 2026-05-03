from .inline import MenuKeyboards, MarketKeyboards, ProfileKeyboards, CashoutKeyboards, CryptoKeyboards
from .reply import MenuReplyKeyboards


class InlineKeyboards:
    def __init__(self):
        self.menu = MenuKeyboards()
        self.market = MarketKeyboards()
        self.profile = ProfileKeyboards()
        self.cashout = CashoutKeyboards()
        self.crypto = CryptoKeyboards()


class ReplyKeyboards:
    def __init__(self):
        self.menu = MenuReplyKeyboards()


__all__ = ["InlineKeyboards", "ReplyKeyboards"]