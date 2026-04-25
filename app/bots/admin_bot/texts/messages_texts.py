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

    PAYMENT_LINK = "Ваши реквизиты для оплаты:\n\n{url}"

    LINK_SENT = "Ссылка успешно отправлена пользователю {user_id}."

    NO_PENDING_PAYMENT = "У пользователя нет активного заказа."


class VerifyTexts:
    """Тексты раздела проверки оплаты"""

    NO_PAYMENTS = "У пользователя нет заказов на проверке."

    ORDERS_LIST = "Заказы пользователя <code>{user_id}</code>:"

    ORDER_DETAIL = (
        "Заказ №{id}\n\n"
        "Пользователь: <code>{user_id}</code>\n"
        "Банк: <b>{bank}</b>\n"
        "Сумма: <b>{price} ₽</b>\n"
        "Количество: <b>{amount} шт.</b>"
    )

    PAYMENT_CONFIRMED = "Оплата подтверждена."

    PAYMENT_COMPLETED = "Оплата прошла. В личном кабинете вы всегда сможете получить доступ к ключам."


class MiscTexts:
    """Общие тексты"""

    ENTER_USER_ID = "Введите Telegram ID пользователя:"
    
    INVALID_USER_ID = "ID должен быть числом."


class Texts:
    """Все тексты"""
    menu = MenuTexts
    link = LinkTexts
    verify = VerifyTexts
    misc = MiscTexts