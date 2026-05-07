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
    hash_length:  int | str   # число или диапазон "87-88"
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


# ─── Валидация ───────────────────────────────────────────────────────────────

def _parse_length(hash_length: int | str) -> tuple[int, int]:
    """Парсит hash_length: число или строку 'min-max'. Возвращает (min, max)."""
    if isinstance(hash_length, int):
        return hash_length, hash_length
    parts = str(hash_length).split("-")
    if len(parts) == 2:
        return int(parts[0]), int(parts[1])
    n = int(parts[0])
    return n, n


def validate_tx_hash(raw: str, network_id: str) -> tuple[bool, str]:
    """
    Очищает хэш от пробелов и проверяет длину для указанной сети.
    Возвращает (валидный, очищенный хэш).
    """
    network = get_network_by_id(network_id)
    if not network:
        return False, raw

    tx_hash = raw.strip().replace(" ", "")
    min_len, max_len = _parse_length(network.hash_length)
    return min_len <= len(tx_hash) <= max_len, tx_hash