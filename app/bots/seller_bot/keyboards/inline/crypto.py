from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.utils import get_networks_for_seller
from .base import BaseInlineKeyboard


class CryptoKeyboards(BaseInlineKeyboard):
    """Клавиатуры крипто вывода для seller_bot."""

    def network_list(self) -> InlineKeyboardMarkup:
        """Список сетей в порядке seller_order + кнопка Назад."""
        networks = get_networks_for_seller()
        rows = [
            [InlineKeyboardButton(
                text=n.name,
                callback_data=f"cashout_network_{n.id}",
            )]
            for n in networks
        ]
        rows.append([InlineKeyboardButton(
            text=self.texts.misc.BACK,
            callback_data="cashout_crypto",
        )])
        return InlineKeyboardMarkup(inline_keyboard=rows)