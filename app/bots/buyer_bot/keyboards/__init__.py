from .inline import MenuKeyboards, ProfileKeyboards, WholesaleKeyboards, PaymentKeyboards


class InlineKeyboards:
    def __init__(self):
        self.menu = MenuKeyboards()
        self.profile = ProfileKeyboards()
        self.wholesale = WholesaleKeyboards()
        self.payment = PaymentKeyboards()


__all__ = ["InlineKeyboards"]
