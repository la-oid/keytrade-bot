class MenuTexts:
    """Тексты меню"""

    START_TEXT = "Добрый день! Вас приветствует бот по продаже ключей."

    PROFILE_TEXT = (
        "ID: {user_id}\n"
        "Список заказов:\n\n"
        "{orders}"
    )

    ABOUT_TEXT = "О магазине"

    SUPPORT_TEXT = "Поддержка"


class WholesaleTexts:
    """Тексты, связанные с оптом"""

    WHOLESALE_TEXT = (
        "Количество: <b>{amount} шт.</b>\n"
        "Сумма: <b>{price} ₽</b>"
    )

    ORDER_CREATED_TEXT = "Заказ на <b>{amount} шт.</b> создан!"


class PaymentTexts:
    """Тексты, связанные с оплатой"""

    CHOOSE_METHOD = "Выберите способ оплаты:"

    CHOOSE_BANK = "Выберите банк:"

    PENDING_TEXT = (
        "Количество: <b>{amount} шт.</b>\n"
        "Сумма: <b>{price} ₽</b>\n"
        "Банк: <b>{bank}</b>\n\n"
        "⏳ Ожидайте реквизиты для оплаты."
    )

    CONFIRM_CANCEL_TEXT = "Вы уверены, что хотите отменить оплату?"

    ADMIN_NOTIFY = (
        "💰 Новый заказ на оплату\n\n"
        "Пользователь: <b>{name}</b> (ID: <code>{user_id}</code>)\n"
        "Банк: <b>{bank}</b>\n"
        "Сумма: <b>{price} ₽</b>\n"
        "Количество: <b>{amount} шт.</b>"
    )

    ADMIN_CANCELLED = (
        "❌ ЗАКАЗ ОТМЕНЁН\n\n"
        "Пользователь: <b>{name}</b> (ID: <code>{user_id}</code>)\n"
        "Банк: <b>{bank}</b>\n"
        "Сумма: <b>{price} ₽</b>\n"
        "Количество: <b>{amount} шт.</b>"
    )

    CANCELLED_TEXT = "Заказ отменён."

    PAYMENT_PAGE = (
        "Заказ номер: <code>{payment_id}</code>\n\n"
        "Внимание, переводите только с указанного вами ранее банка! "
        "В ином случае заказ обработан не будет."
    )

    WAITING_PDF = (
        "Пожалуйста, приложите квитанцию об оплате в формате PDF.\n"
        "В противном случае оплата не будет засчитана."
    )


class MiscTexts:
    """Общие тексты"""
    pass


class Texts:
    """Все тексты"""
    menu = MenuTexts
    wholesale = WholesaleTexts
    payment = PaymentTexts
    misc = MiscTexts
