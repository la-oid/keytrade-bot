class MenuTexts:
    """Тексты меню"""
    
    START_TEXT = "Добро пожаловать в админ-панель."


class LinkTexts:
    """Тексты для создания ссылки"""

    ENTER_DATA = (
        "Введите данные через запятую:\n\n"
        "<b>Банк, Сумма, Телефон/Карта</b>\n\n"
        "Пример: <code>Сбербанк, 5000, 79001234567</code>"
    )

    INVALID_DATA = "Неверный формат. Введите 3 параметра через запятую."

    ENTER_USER_ID = "Введите Telegram ID пользователя:"

    INVALID_USER_ID = "ID должен быть числом."

    PAYMENT_LINK = "Ваши реквизиты для оплаты:\n\n{url}"

    LINK_SENT = "Ссылка успешно отправлена пользователю {user_id}."


class MiscTexts:
    """Общие тексты"""
    pass


class Texts:
    """Все тексты"""
    menu = MenuTexts
    link = LinkTexts
    misc = MiscTexts