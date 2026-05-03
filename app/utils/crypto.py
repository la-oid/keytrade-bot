import json
from dataclasses import dataclass
from functools import lru_cache

from app.shared.paths import CRYPTO_NETWORKS_FILE


@dataclass
class CryptoNetwork:
    id:           str
    name:         str
    address:      str
    hash_format:  str
    hash_length:  int
    buyer_order:  int
    seller_order: int


# ─── Загрузка ────────────────────────────────────────────────────────────────

@lru_cache(maxsize=1)
def load_networks() -> list[CryptoNetwork]:
    """Загружает сети из JSON один раз и кэширует."""
    with open(CRYPTO_NETWORKS_FILE, encoding="utf-8") as f:
        data = json.load(f)
    return [CryptoNetwork(**item) for item in data]


# ─── Фильтрация и сортировка ─────────────────────────────────────────────────

def get_networks_for_bot(order_field: str) -> list[CryptoNetwork]:
    """
    Универсальная функция — возвращает сети для указанного бота.
    order_field: 'buyer_order' или 'seller_order'
    Сети с order == 0 или None — скрываются.
    """
    return sorted(
        [n for n in load_networks() if getattr(n, order_field, 0)],
        key=lambda n: getattr(n, order_field),
    )


def get_networks_for_buyer() -> list[CryptoNetwork]:
    """Возвращает сети для buyer_bot."""
    return get_networks_for_bot("buyer_order")


def get_networks_for_seller() -> list[CryptoNetwork]:
    """Возвращает сети для seller_bot."""
    return get_networks_for_bot("seller_order")


# ─── Поиск ───────────────────────────────────────────────────────────────────

def get_network_by_id(network_id: str) -> CryptoNetwork | None:
    """Возвращает сеть по ID или None."""
    return next((n for n in load_networks() if n.id == network_id), None)