class MenuTexts:
    """Тексты меню"""
    
    START_TEXT = "Добро пожаловать в админ-панель."


class VerifyTexts:
    """Тексты раздела проверки оплаты"""

    NO_PAYMENTS = "У пользователя нет заказов на проверке."

    ORDERS_LIST = "Заказы пользователя <code>{user_id}</code>:"

    ORDER_DETAIL_SPB = (
        "Заказ №{id}\n\n"
        "Пользователь: <code>{user_id}</code>\n"
        "Сумма: <b>{price:.2f} ₽</b>\n"
        "Количество: <b>{amount} шт.</b>"
    )

    ORDER_DETAIL_CRYPTO = (
        "Заказ №{id}\n\n"
        "Пользователь: <code>{user_id}</code>\n"
        "Сеть: <b>{network}</b>\n"
        "Сумма: <b>{price:.2f} ₽</b> / <b>{usdt_amount} USDT</b>\n"
        "Количество: <b>{amount} шт.</b>\n"
        "Хэш: <code>{tx_hash}</code>"
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
 
    CASHOUT_DETAIL_SPB = (
        "Заявка #{id}\n\n"
        "Пользователь: <code>{user_id}</code>\n"
        "Сумма: <b>{amount:.2f} ₽</b>\n"
        "Карта: <code>{card}</code>"
    )

    CASHOUT_DETAIL_CRYPTO = (
        "Заявка #{id}\n\n"
        "Пользователь: <code>{user_id}</code>\n"
        "Сеть: <b>{network}</b>\n"
        "Сумма: <b>{amount:.2f} ₽</b> / <b>{usdt_amount} USDT</b>\n"
        "Кошелёк: <code>{wallet}</code>"
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


class SpecialOfferTexts:
    """Тексты раздела спецпредложений"""
 
    ENTER_DATA = (
        "Введите данные через запятую:\n\n"
        "<b>Кол-во ключей, Время жизни (ч)</b>\n\n"
        "Пример: <code>10, 48</code>"
    )
 
    ENTER_TEXT = "Введите текст спецпредложения:"
 
    CONFIRM_PREVIEW = (
        "Проверьте данные:\n\n"
        "Пользователь: <code>{user_id}</code>\n"
        "Ключей: <b>{keys_count}</b>\n"
        "Время жизни: <b>{lifetime_hours} ч</b>\n"
        "Истекает: <b>{expires_at} UTC</b>\n\n"
        "Текст:\n{custom_text}"
    )
 
    SENT        = "Спецпредложение отправлено пользователю <code>{user_id}</code>."
    SEND_FAILED = "Не удалось отправить пользователю <code>{user_id}</code>. Возможно, он не запускал бот."


class TenderTexts:
    """Тексты раздела тендеров"""

    STATUS      = "Тендер: <b>{current}/{total} шт</b>"
    NO_ACTIVE   = "Нет активного тендера."

    ENTER_ADD   = "Сколько добавить?"
    ENTER_COUNT = "Позиций в тендере?"

    INVALID_COUNT = "Введите целое число больше 0."

    ADDED   = "Добавлено <b>{amount}</b>. Тендер: <b>{current}/{total} шт</b>"
    QUEUED  = "Тендер поставлен в очередь. Позиций: <b>{total}</b>"
    LAUNCHED = "Тендер запущен. Позиций: <b>{total}</b>"

    NOTIFY  = "Тендер: <b>{current}/{total} шт</b>"


class BroadcastTexts:
    """Тексты раздела рассылки"""

    ENTER_TEXT = "Введите текст уведомления:"

    CONFIRM_PREVIEW = (
        "Проверьте текст рассылки:\n\n"
        "{text}"
    )

    SENDING = "Рассылка выполняется..."

    DONE = (
        "Рассылка завершена.\n\n"
        "Отправлено: <b>{sent}</b>\n"
        "Не доставлено: <b>{failed}</b>"
    )


class MiscTexts:
    """Общие тексты"""

    ENTER_USER_ID = "Введите Telegram ID пользователя:"

    INVALID_USER_ID = "ID должен быть числом."


class Texts:
    """Все тексты"""
    menu = MenuTexts
    verify = VerifyTexts
    order = OrderTexts
    cashout = CashoutTexts
    block = BlockTexts
    account = AccountTexts
    special_offer = SpecialOfferTexts
    tender = TenderTexts
    broadcast = BroadcastTexts
    misc = MiscTexts
