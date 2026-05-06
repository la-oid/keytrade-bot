class MenuTexts:
    """Тексты меню"""

    START_TEXT = "Добрый день! Вас приветствует бот по продаже ключей."

    PROFILE_TEXT = "ID: <code>{user_id}</code>"

    ABOUT_TEXT = "О магазине"

    SUPPORT_TEXT = "Поддержка"


class ProfileTexts:
    """Тексты профиля и заказов"""

    ORDERS_LIST = "Ваши заказы:"

    NO_ORDERS = "У вас пока нет заказов."

    ORDER_PENDING = (
        "Ваш заказ находится в очереди на обработку, пожалуйста, ожидайте.\n"
        "При возникновении вопросов, пишите в поддержку."
    )

    ORDER_COMPLETED = "Заказ выполнен.\n\nПолучено: <b>{amount}</b> ключей."


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

    CONFIRM_CANCEL_TEXT = "Вы уверены, что хотите отменить оплату?"
    CANCELLED_TEXT = "Заказ отменён."

    PAYMENT_EXPIRED = (
        "⚠️ У заказа <code>{payment_id}</code> истек срок оплаты\n\n"
        "Если у вас возникла одна из проблем:\n"
        "🔹 Не зачислилась оплата\n"
        "🔹 Не выдались реквизиты\n"
        "🔹 Не вышло сделать перевод\n\n"
        "Обратитесь к поддержке платежной системы\n"
        "💬 Прямой контакт: @{support}\n\n"
        "❤️ Приносим свои извинения, если вы столкнулись с проблемами при оплате. "
        "С радостью поможем решить их вам!"
    )

    PAYMENT_PAGE = (
        "💳 Пополнение баланса: <code>{payment_id}</code>\n\n"
        "Сумма к оплате: <b>{price} ₽</b>\n"
        "<blockquote>ℹ️ Сумма пополнения указана без учёта комиссии платёжной системы, "
        "которая добавляется при оплате. Мы делим эту комиссию с вами, чтобы сохранять "
        "для вас низкие цены и качественный сервис.</blockquote>\n\n"
        "Время на оплату: <b>{minutes} минут</b>\n"
        "Оплатить до <b>{deadline} (МСК)</b>"
    )

    WAITING_PDF = (
        "Пожалуйста, приложите квитанцию об оплате в формате PDF.\n"
        "В противном случае оплата не будет засчитана."
    )

    WRONG_FORMAT = "Неверный формат. Пришлите файл в формате PDF."

    ADMIN_PDF_RECEIVED = (
        "💳 Заказ оплачен\n\n"
        "Пользователь: <b>{name}</b> (ID: <code>{user_id}</code>)\n"
        "Сумма: <b>{price} ₽</b>\n"
        "Количество: <b>{amount} шт.</b>\n"
        "ID платежа: <code>{payment_id}</code>"
    )

    ADMIN_CANCELLED = (
        "❌ ЗАКАЗ ОТМЕНЁН\n\n"
        "Пользователь: <b>{name}</b> (ID: <code>{user_id}</code>)\n"
        "Сумма: <b>{price} ₽</b>\n"
        "Количество: <b>{amount} шт.</b>"
    )

    SESSION_DEAD  = "Сервис оплаты временно недоступен. Попробуйте позже."
    PAYMENT_ERROR = "Ошибка создания платежа. Попробуйте позже."


class SpecialOfferTexts:
    """Тексты спецпредложений"""

    OFFER_TEXT = (
        "🎁 <b>Спецпредложение</b>\n\n"
        "Количество ключей: <b>{keys_count}</b>\n"
        "Итого к оплате: <b>{total_price} ₽</b>\n\n"
        "Предложение действует до: <b>{expires_at} UTC</b>"
    )

    OFFER_DECLINED = (
        "Предложение ещё действует до <b>{expires_at} UTC</b>.\n\n"
        "Посмотреть предложение вы сможете в личном кабинете (Профиль)."
    )

    NO_OFFER = "Активных спецпредложений нет."


class CryptoTexts:
    """Тексты крипто оплаты"""
 
    CHOOSE_NETWORK = (
        "Выберите сеть для оплаты.\n\n"
        "Внимание, вывод производится исключительно через USDT.\n"
        "Текущий курс: <b>{rate} ₽</b> за 1 USDT.\n"
        "Сумма к оплате: <b>{usdt_amount} USDT</b>"
    )
 
    NETWORK_ADDRESS = (
        "Сеть: <b>{network}</b>\n\n"
        "Адрес кошелька:\n"
        "<code>{address}</code>\n\n"
        "Сумма к оплате: <b>{usdt_amount} USDT</b>\n\n"
        "Скопируйте адрес и переведите точную сумму.\n"
        "После оплаты нажмите «Я оплатил»."
    )
 
    WAITING_HASH = (
        "Скиньте хэш транзакции.\n\n"
        "Пример формата: <code>{hash_format}</code>\n"
        "Пробелы будут удалены автоматически."
    )
 
    INVALID_HASH = (
        "Неверный формат хэша.\n\n"
        "Ожидаемый формат: <code>{hash_format}</code>\n"
        "Отправьте хэш ещё раз."
    )
 
    ADMIN_NOTIFY = (
        "💎 Новый крипто заказ\n\n"
        "Пользователь: <b>{name}</b> (ID: <code>{user_id}</code>)\n"
        "Сеть: <b>{network}</b>\n"
        "Сумма: <b>{price:.2f} ₽</b> / <b>{usdt_amount} USDT</b>\n"
        "Количество: <b>{amount} шт.</b>\n"
        "ID платежа: <code>{payment_id}</code>\n"
        "Хэш: <code>{tx_hash}</code>"
    )
 
    RATE_ERROR = "Не удалось получить курс. Попробуйте позже."


class MiscTexts:
    """Общие тексты"""
    pass


class Texts:
    """Все тексты"""
    menu = MenuTexts
    profile = ProfileTexts
    wholesale = WholesaleTexts
    payment = PaymentTexts
    special_offer = SpecialOfferTexts
    crypto = CryptoTexts
    misc = MiscTexts
