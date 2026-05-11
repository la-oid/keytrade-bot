class MenuTexts:
    """Тексты меню"""
 
    START_TEXT = (
        "Добрый день! Вас приветствует бот-агрегатор.\n\n"
        "Выберите раздел из меню снизу."
    )
 
    ABOUT_TEXT = (
        "Мы — агрегаторная платформа, которая помогает продавцам "
        "сдавать ключи в выгодные паи и получать стабильный доход.\n\n"
        "Подробнее о нас и условиях работы скоро здесь."
    )
 
    SUPPORT_TEXT = "Если у вас вопрос или проблема — напишите нам: @{username}"


class ProfileTexts:
    """Тексты профиля"""
 
    PROFILE_TEXT = (
        "<b>ID:</b> <code>{user_id}</code>\n"
        "<b>Баланс:</b> {balance:.2f} ₽\n"
        "{frozen_line}"
        "<b>Выполнено заказов:</b> {completed}"
    )

    FROZEN_LINE = "<b>Заморожено:</b> {frozen:.2f} ₽\n"


class CashoutTexts:
    """Тексты вывода средств"""
 
    CHOOSE_AMOUNT = (
        "Сколько хотите вывести?\n\n"
        "Текущий баланс: <b>{balance:.2f} ₽</b>"
    )
 
    ENTER_AMOUNT = (
        "◆ Введите сумму для вывода.\n"
        "◆ Минимум - <b>{min} ₽</b>, шаг - <b>{step} ₽</b>, не более текущего баланса."
    )

    INVALID_AMOUNT = (
        "◆ Неверная сумма.\n\n"
        "Введите значение, <b>кратное {step} ₽</b>, от <b>{min} ₽</b> "
        "и не превышающее текущий баланс."
    )
 
    CHOOSE_METHOD = "Выберите метод получения средств:"
 
    ENTER_CARD = (
        "Введите номер карты (16 цифр).\n\n"
        "Пример: <code>1234567890123456</code>"
    )
 
    CREATED = (
        "Заявка #{cashout_id} создана.\n\n"
        "Сумма: <b>{amount:.2f} ₽</b>\n"
        "Карта: <b>{card}</b>\n\n"
        "Средства заморожены. Статус можно отследить в личном кабинете."
    )

    ENTER_STATUS_ID = "Введите номер заявки:"

    STATUS_INFO = (
        "Заявка #{cashout_id}\n\n"
        "Сумма: <b>{amount:.2f} ₽</b>\n"
        "Статус: <b>{status}</b>"
    )

    HISTORY_TITLE = "Ваши выводы:"

    HISTORY_DETAIL = (
        "Заявка #{id}\n\n"
        "Сумма: <b>{amount:.2f} ₽</b>\n"
        "Карта: <b>{card}</b>\n"
        "Статус: <b>{status}</b>"
    )

    CASHOUT_COMPLETED_NOTIFY = (
        "Заявка #{id} выполнена.\n"
        "Сумма <b>{amount:.2f} ₽</b> переведена."
    )
    
    ADMIN_NOTIFY_CARD = (
        "💳 Заявка на вывод (карта)\n\n"
        "Пользователь: <code>{user_id}</code>\n"
        "Сумма: <code>{amount:.2f}</code> ₽\n"
        "Карта: <code>{card}</code>\n"
        "ID заявки: <code>{cashout_id}</code>"
    )

    STATUS_PENDING   = "В очереди на вывод"
    STATUS_COMPLETED = "Выполнено"
    STATUS_CANCELLED = "Отменено"
 
    NOT_ENOUGH   = "На балансе недостаточно средств."
    INVALID_CARD   = "Неверный номер карты. Введите 16 цифр без пробелов."
    INVALID_STATUS_ID = "Введите корректный номер заявки."
    STATUS_NOT_FOUND  = "Заявка не найдена."


class MarketTexts:
    """Тексты площадки заказов"""

    MARKET_INTRO = (
        "Здесь вы можете ознакомиться со свободными паями.\n"
        "Выберите подходящий — и сдайте ключи."
    )

    CONFIRM = (
        "Заказ #{id}\n"
        "Ключей нужно сдать: <b>{total_keys}</b>\n\n"
        "Желаете принять данный заказ?"
    )

    SEND_KEYS = (
        "Отправьте ключи файлом <b>.txt</b>.\n\n"
        "Каждый ключ — на отдельной строке. "
        "Всего нужно ровно <b>{total_keys}</b> ключей."
    )

    CHECKING = "Выполняется проверка. Пожалуйста, подождите 15–45 секунд..."

    SUCCESS = "Ключи зачислены. На баланс начислено <b>{payout:.2f} ₽</b>."

    INVALID_FORMAT = (
        "Неправильный формат либо некорректное количество ключей.\n\n"
        "Пришлите .txt файл — один ключ на строку, "
        "ровно столько, сколько указано в пае."
    )

    ORDER_NOT_FOUND = "Этот пай больше недоступен."


class CryptoTexts:
    """Тексты вывода средств — крипта"""
 
    CHOOSE_NETWORK = (
        "Выберите сеть для вывода.\n\n"
        "Внимание, вывод производится исключительно через USDT.\n"
        "Текущий курс: <b>{rate:.2f} ₽</b> за 1 USDT.\n\n"
        "Сумма к выводу: <b>{amount:.2f} ₽</b> / <b>{usdt_amount:.4f} USDT</b>"
    )
 
    ENTER_WALLET = (
        "Сеть: <b>{network}</b>\n\n"
        "Введите адрес вашего кошелька для получения USDT."
    )
 
    CREATED_CRYPTO = (
        "Заявка #{cashout_id} создана.\n\n"
        "Сумма: <b>{amount:.2f} ₽</b> / <b>{usdt_amount:.4f} USDT</b>\n"
        "Сеть: <b>{network}</b>\n"
        "Кошелёк: <code>{wallet}</code>\n\n"
        "Средства списаны. Статус можно отследить в личном кабинете."
    )
 
    ADMIN_NOTIFY_CRYPTO = (
        "💎 Заявка на вывод (крипта)\n\n"
        "Пользователь: <code>{user_id}</code>\n"
        "Сумма: <b>{amount:.2f} ₽</b> / <b>{usdt_amount:.4f} USDT</b>\n"
        "Сеть: <b>{network}</b>\n"
        "Кошелёк: <code>{wallet}</code>\n"
        "ID заявки: <code>{cashout_id}</code>"
    )
 
    HISTORY_DETAIL_CRYPTO = (
        "Заявка #{id}\n\n"
        "Сумма: <b>{amount:.2f} ₽</b> / <b>{usdt_amount:.4f} USDT</b>\n"
        "Сеть: <b>{network}</b>\n"
        "Кошелёк: <code>{wallet}</code>\n"
        "Статус: <b>{status}</b>"
    )
 
    INVALID_WALLET = "Адрес кошелька должен содержать минимум 20 символов."
    RATE_ERROR     = "Не удалось получить курс. Попробуйте позже."


class MiscTexts:
    """Общие тексты"""
    
    pass


class Texts:
    """Все тексты"""
    menu = MenuTexts
    profile = ProfileTexts
    cashout = CashoutTexts
    market  = MarketTexts
    crypto = CryptoTexts
    misc = MiscTexts
