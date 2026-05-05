class MenuButtonTexts:
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


class AccountButtonTexts:
    ADD         = "➕ Добавить"
    SUBTRACT    = "➖ Отнять"
    FREEZE_ALL  = "🔒 Заморозить всё"
    UNFREEZE_ALL = "🔓 Разморозить всё"
    CONFIRM     = "✅ Подтвердить"


class SpecialOfferButtonTexts:
    CONFIRM = "✅ Да, отправить"
    RETRY   = "✏️ Ввести заново"


class MiscButtonTexts:
    BACK = "← Назад"


class ButtonTexts:
    menu = MenuButtonTexts
    verify = VerifyButtonTexts
    order = OrderButtonTexts
    cashout = CashoutButtonTexts
    block = BlockButtonTexts
    account = AccountButtonTexts
    special_offer = SpecialOfferButtonTexts
    misc = MiscButtonTexts