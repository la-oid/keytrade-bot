from .inline import MenuKeyboards, ProfileKeyboards, WholesaleKeyboards, PaymentKeyboards
from .reply import MenuReplyKeyboards


class InlineKeyboards:
    def __init__(self):
        self.menu = MenuKeyboards()
        self.profile = ProfileKeyboards()
        self.wholesale = WholesaleKeyboards()
        self.payment = PaymentKeyboards()


class ReplyKeyboards:
    def __init__(self):
        self.menu = MenuReplyKeyboards()


__all__ = ["InlineKeyboards", "ReplyKeyboards"]