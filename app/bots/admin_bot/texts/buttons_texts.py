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
    BACK      = "← Назад"
    DELETE    = "Удалить"
    ORDER_ROW = "#{id} — {total_keys} ключей · {price_per_key} ₽/шт"


class MiscButtonTexts:
    pass


class ButtonTexts:
    menu = MenuButtonTexts
    verify = VerifyButtonTexts
    order = OrderButtonTexts
    misc = MiscButtonTexts