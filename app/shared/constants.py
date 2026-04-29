KEY_PRICE = 50  # Фиксированная цена одного ключа при покупке

MEDIUM = {"min": 100, "max": 500, "step": 50}
LARGE = {"min": 1000, "step": 100}

BANKS = ["Сбербанк", "Тинькофф"]

PDF_STORAGE = "storage/pdf"

# ── Паи (тендеры) ────────────────────────────────────────────────────────────
PIE_KEYS_MIN           = 300    # Минимум ключей в фейке (нижний диапазон)
PIE_KEYS_MID           = 1000   # Граница раздела диапазонов
PIE_KEYS_MAX           = 1800   # Максимум ключей в фейке (верхний диапазон)
PIE_KEYS_STEP          = 50     # Шаг (кратность) ключей
PIE_MIN_LIFETIME_HOURS = 1      # Минимальное время жизни пая (ч)
PIE_MAX_LIFETIME_HOURS = 4      # Максимальное время жизни пая (ч)
PIE_FAKE_LOW_COUNT     = 5      # Фиксированное кол-во фейков [PIE_KEYS_MIN, PIE_KEYS_MID]
PIE_FAKE_HIGH_COUNT    = 3      # Фиксированное кол-во фейков [PIE_KEYS_MID, PIE_KEYS_MAX]

KEY_CHECK_DURATION = 15     # Длительность проверки ключей в seller-боте (сек)

CASHOUT_STEP = 50           # Минимальный шаг суммы вывода (кратность)
