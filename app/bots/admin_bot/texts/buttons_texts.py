class MenuButtonTexts:
    GET_LINK = "Получение ссылки"
    CHECK_PAYMENT = "Проверка оплаты"
    USER_ACCOUNT = "Управление счетом"
    SPECIAL_OFFERS = "Спецпредложения"
    CREATE_PIE = "Паи"
    PAYOUTS = "Заявки на выплату"
    BLOCK_USER = "Блокировка"


class VerifyButtonTexts:
    VERIFY = "Проверка оплаты"
    PAYMENT_OK = "Оплата прошла"
    ORDER = "#{id} — {amount} шт., {price} ₽"


class OrderButtonTexts:
    CREATE    = "Создать пай"
    DELETE    = "Удалить"
    ORDER_ROW = "#{id} — {total_keys} ключей"


class CashoutButtonTexts:
    COMPLETE    = "Выполнен"
    CASHOUT_ROW = "#{id} — {amount:.2f} ₽"


class BlockButtonTexts:
    BLOCK   = "🔒 Заблокировать"
    UNBLOCK = "🔓 Разблокировать"


class MiscButtonTexts:
    BACK = "← Назад"


class ButtonTexts:
    menu = MenuButtonTexts
    verify = VerifyButtonTexts
    order = OrderButtonTexts
    cashout = CashoutButtonTexts
    block = BlockButtonTexts
    misc = MiscButtonTexts