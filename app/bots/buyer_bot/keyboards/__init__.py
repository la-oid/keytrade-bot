from .inline import MenuKeyboards, WholesaleKeyboards, PaymentKeyboards


class InlineKeyboards:
    def __init__(self):
        self.menu = MenuKeyboards()
        self.wholesale = WholesaleKeyboards()
        self.payment = PaymentKeyboards()


__all__ = ["InlineKeyboards"]
