from .inline import MenuKeyboards, MiscKeyboards, WholesaleKeyboards, PaymentKeyboards


class InlineKeyboards:
    def __init__(self):
        self.menu = MenuKeyboards()
        self.misc = MiscKeyboards()
        self.wholesale = WholesaleKeyboards()
        self.payment = PaymentKeyboards()


__all__ = ["InlineKeyboards"]
