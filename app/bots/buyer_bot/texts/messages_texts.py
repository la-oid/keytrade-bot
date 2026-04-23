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

    WHOLESALE_TEXT = (
        "Количество: <b>{amount} шт.</b>\n"
        "Сумма: <b>{price} ₽</b>"
    )

    ORDER_CREATED_TEXT = "Заказ на <b>{amount} шт.</b> создан!"


class MiscTexts:
    """Общие тексты"""
    pass


class ErrorsTexts:
    """Тексты ошибок"""
    pass


class Texts:
    """Все тексты"""
    menu = MenuTexts
    errors = ErrorsTexts
    misc = MiscTexts