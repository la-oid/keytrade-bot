from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.utils import get_networks_for_buyer
from .base import BaseInlineKeyboard


class CryptoKeyboards(BaseInlineKeyboard):
    """Клавиатуры крипто оплаты."""

    def network_list(self) -> InlineKeyboardMarkup:
        """Список сетей в порядке buyer_order + кнопка Назад."""
        networks = get_networks_for_buyer()
        rows = [
            [InlineKeyboardButton(
                text=n.name,
                callback_data=f"crypto_network_{n.id}",
            )]
            for n in networks
        ]
        rows.append([InlineKeyboardButton(
            text=self.texts.misc.BACK,
            callback_data="confirm_order",
        )])
        return InlineKeyboardMarkup(inline_keyboard=rows)

    def network_actions(self, network_id: str) -> InlineKeyboardMarkup:
        """Кнопки после выбора сети: Скопировать, Я оплатил, Назад."""
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(
                    text=self.texts.crypto.PAID,
                    callback_data=f"crypto_paid_{network_id}",
                )],
                [InlineKeyboardButton(
                    text=self.texts.misc.BACK,
                    callback_data="pay_crypto",
                )],
            ]
        )