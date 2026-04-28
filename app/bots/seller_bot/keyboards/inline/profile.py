from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from .base import BaseInlineKeyboard


class ProfileKeyboards(BaseInlineKeyboard):
    """Клавиатуры профиля."""

    def profile(self) -> InlineKeyboardMarkup:
        """Профиль: Вывод средств и Узнать статус заявки."""
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(
                    text=self.texts.profile.WITHDRAW,
                    callback_data="profile_withdraw",
                )],
                [InlineKeyboardButton(
                    text=self.texts.profile.WITHDRAW_STATUS,
                    callback_data="profile_withdraw_status",
                )],
            ]
        )