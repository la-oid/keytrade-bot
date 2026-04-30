from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from .base import BaseInlineKeyboard


class AccountKeyboards(BaseInlineKeyboard):
    """Клавиатуры раздела управления счётом."""

    def account_menu(self, user_id: int) -> InlineKeyboardMarkup:
        """Главное меню: Добавить, Отнять, Заморозить, Разморозить, Назад."""
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=self.texts.account.ADD,
                        callback_data=f"account_add_{user_id}",
                    ),
                    InlineKeyboardButton(
                        text=self.texts.account.SUBTRACT,
                        callback_data=f"account_subtract_{user_id}",
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text=self.texts.account.FREEZE_ALL,
                        callback_data=f"account_freeze_{user_id}",
                    ),
                    InlineKeyboardButton(
                        text=self.texts.account.UNFREEZE_ALL,
                        callback_data=f"account_unfreeze_{user_id}",
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text=self.texts.misc.BACK,
                        callback_data="account_back",
                    ),
                ],
            ]
        )

    def confirm(self, user_id: int, action: str, amount: float) -> InlineKeyboardMarkup:
        """Подтверждение действия."""
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(
                    text=self.texts.account.CONFIRM,
                    callback_data=f"account_confirm_{action}_{user_id}_{amount}",
                )],
                [InlineKeyboardButton(
                    text=self.texts.misc.BACK,
                    callback_data=f"account_menu_{user_id}",
                )],
            ]
        )