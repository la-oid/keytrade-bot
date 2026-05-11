from .inline import (
    MenuKeyboards,
    VerifyKeyboards,
    OrderKeyboards,
    CashoutKeyboards,
    BlockKeyboards,
    AccountKeyboards,
    SpecialOfferKeyboards,
    BroadcastKeyboards,
    TenderKeyboards,
)
from .reply import MenuReplyKeyboards


class InlineKeyboards:
    def __init__(self):
        self.menu = MenuKeyboards()
        self.verify = VerifyKeyboards()
        self.order = OrderKeyboards()
        self.cashout = CashoutKeyboards()
        self.block = BlockKeyboards()
        self.account = AccountKeyboards()
        self.special_offer = SpecialOfferKeyboards()
        self.broadcast = BroadcastKeyboards()
        self.tender = TenderKeyboards()


class ReplyKeyboards:
    def __init__(self):
        self.menu = MenuReplyKeyboards()


__all__ = ["InlineKeyboards", "ReplyKeyboards"]
