from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from .base import BaseInlineKeyboard


class BlockKeyboards(BaseInlineKeyboard):
    """Клавиатуры раздела блокировки."""

    def actions(self, user_id: int, is_blocked: bool) -> InlineKeyboardMarkup:
        """Показывает кнопку в зависимости от текущего статуса юзера."""
        if is_blocked:
            button = InlineKeyboardButton(
                text=self.texts.block.UNBLOCK,
                callback_data=f"unblock_user_{user_id}",
            )
        else:
            button = InlineKeyboardButton(
                text=self.texts.block.BLOCK,
                callback_data=f"block_user_{user_id}",
            )
        return InlineKeyboardMarkup(inline_keyboard=[[button]])