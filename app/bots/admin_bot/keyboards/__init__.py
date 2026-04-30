from .inline import MenuKeyboards, VerifyKeyboards, OrderKeyboards, CashoutKeyboards, BlockKeyboards
from .reply import MenuReplyKeyboards


class InlineKeyboards:
    def __init__(self):
        self.menu = MenuKeyboards()
        self.verify = VerifyKeyboards()
        self.order = OrderKeyboards()
        self.cashout = CashoutKeyboards()
        self.block = BlockKeyboards()


class ReplyKeyboards:
    def __init__(self):
        self.menu = MenuReplyKeyboards()


__all__ = ["InlineKeyboards", "ReplyKeyboards"]
