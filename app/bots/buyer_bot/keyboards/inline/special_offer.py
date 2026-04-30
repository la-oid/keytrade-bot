from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from .base import BaseInlineKeyboard


class SpecialOfferKeyboards(BaseInlineKeyboard):
    """Клавиатуры спецпредложений."""

    def offer_actions(self) -> InlineKeyboardMarkup:
        """Принять / Подумаю."""
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(
                    text=self.texts.special_offer.ACCEPT,
                    callback_data="offer_accept",
                )],
                [InlineKeyboardButton(
                    text=self.texts.special_offer.DECLINE,
                    callback_data="offer_decline",
                )],
            ]
        )

    def back_to_profile(self) -> InlineKeyboardMarkup:
        """Назад в профиль."""
        return InlineKeyboardMarkup(
            inline_keyboard=[[
                InlineKeyboardButton(
                    text=self.texts.special_offer.BACK_TO_PROFILE,
                    callback_data="profile",
                )
            ]]
        )