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


class OrderTexts:
    """Тексты раздела паёв"""
 
    CURRENT_ORDERS = "Текущие паи: {count}"
 
    ENTER_CREATE_DATA = (
        "Введите данные через запятую:\n\n"
        "<b>Кол-во ключей, Время жизни (ч)</b>\n\n"
        "Пример: <code>500, 3</code>"
    )
 
    ORDER_CREATED = (
        "Пай #{order_id} создан.\n\n"
        "Ключей: <b>{total_keys}</b>\n"
        "Истекает: <b>{expires_at} UTC</b>"
    )
 
    DELETE_LIST = "Выберите пай для удаления:"
 
    ORDER_DELETED = (
        "Пай #{order_id} удалён.\n"
        "Ключей было: <b>{total_keys}</b>"
    )
 
    ORDER_NOT_FOUND = "Пай не найден — возможно, уже истёк."
    INVALID_DATA    = (
        "Неверный формат. Введите два значения через запятую.\n"
        "Пример: <code>500, 3</code>"
    )


class CashoutTexts:
    """Тексты раздела заявок на выплату"""
 
    CURRENT_CASHOUTS = "Текущие заявки на выплату:"
 
    CASHOUT_DETAIL = (
        "Заявка #{id}\n\n"
        "Пользователь: <code>{user_id}</code>\n"
        "Сумма: <b>{amount:.2f} ₽</b>\n"
        "Карта: <code>{card}</code>"
    )
 
    CASHOUT_COMPLETED = "Заявка #{id} выполнена. Сумма: <b>{amount:.2f} ₽</b>"
 
    CASHOUT_NOT_FOUND = "Заявка не найдена или уже обработана."

    CASHOUT_COMPLETED_NOTIFY = (
        "Заявка #{id} выполнена.\n"
        "Сумма <b>{amount:.2f} ₽</b> переведена."
    )


class BlockTexts:
    """Тексты раздела блокировки"""
 
    ENTER_USER_ID = "Введите Telegram ID пользователя:"
 
    USER_NOT_FOUND = "Пользователь не найден."
 
    USER_STATUS = (
        "Пользователь <code>{user_id}</code>\n"
        "Статус: <b>{status}</b>"
    )
 
    STATUS_ACTIVE  = "Активен"
    STATUS_BLOCKED = "Заблокирован"


class AccountTexts:
    """Тексты раздела управления счётом"""
 
    ACCOUNT_INFO = (
        "Пользователь <code>{user_id}</code>\n\n"
        "Баланс: <b>{balance:.2f} ₽</b>\n"
        "Заморожено: <b>{frozen:.2f} ₽</b>"
    )
 
    ENTER_AMOUNT = "Введите сумму:"
 
    CONFIRM_TEXT = (
        "{action} <b>{amount:.2f} ₽</b>\n"
        "Пользователь: <code>{user_id}</code>\n\n"
        "Подтвердить?"
    )
 
    ACTION_ADD      = "Начислить"
    ACTION_SUBTRACT = "Списать"
 
    USER_NOT_FOUND = "Пользователь не найден."
    INVALID_AMOUNT = "Введите корректную сумму (больше 0)."


class MiscTexts:
    """Общие тексты"""

    ENTER_USER_ID = "Введите Telegram ID пользователя:"
    
    INVALID_USER_ID = "ID должен быть числом."


class Texts:
    """Все тексты"""
    menu = MenuTexts
    link = LinkTexts
    verify = VerifyTexts
    order = OrderTexts
    cashout = CashoutTexts
    block = BlockTexts
    account = AccountTexts
    misc = MiscTexts
