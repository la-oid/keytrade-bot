class MenuButtonTexts:
    PROFILE = "Профиль"
    MEDIUM_WHOLESALE = "Средний опт"
    LARGE_WHOLESALE = "Крупный опт"
    ABOUT = "О магазине"
    SUPPORT = "Поддержка"


class ProfileButtonTexts:
    ORDERS = "Мои заказы"
    ORDER = "#{id} — {amount} шт., {price} ₽"
    SUPPORT = "Написать в поддержку"
    SPECIAL_OFFER = "🎁 Спец предложение"


class WholesaleButtonTexts:
    AMOUNT_MINUS = "- {step}"
    AMOUNT_PLUS = "+ {step}"
    CONFIRM_ORDER = "Купить за {price} ₽"


class PaymentButtonTexts:
    SPB = "СБП"
    SBER = "Сбербанк"
    TINKOFF = "Тинькофф"
    CANCEL_PAYMENT = "Отменить оплату"
    CHANGED_MIND = "Я передумал"
    CONFIRM_CANCEL = "Точно отменить"
    CANCEL_ACTIVE = "Отменить заказ"
    OPEN_LINK = "Открыть ссылку"
    SENT = "Перевел"


class SpecialOfferButtonTexts:
    ACCEPT          = "Принять"
    DECLINE         = "Подумаю"
    BACK_TO_PROFILE = "← В профиль"


class MiscButtonTexts:
    BACK = "← Назад"


class ButtonTexts:
    menu = MenuButtonTexts
    profile = ProfileButtonTexts
    wholesale = WholesaleButtonTexts
    payment = PaymentButtonTexts
    special_offer = SpecialOfferButtonTexts
    misc = MiscButtonTexts