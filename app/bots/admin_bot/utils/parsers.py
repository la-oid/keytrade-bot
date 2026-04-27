def parse_order_create(text: str) -> tuple[int, float, int] | None:
    """
    Парсит строку вида 'кол-во, цена, часы'.
    Возвращает (keys_count, price, lifetime_hours) или None при ошибке.
    """
    parts = text.strip().replace(" ", "").split(",")

    if len(parts) != 3:
        return None

    try:
        keys_count     = int(parts[0])
        price          = float(parts[1])
        lifetime_hours = int(parts[2])

        if keys_count <= 0 or price <= 0 or lifetime_hours <= 0:
            return None

        return keys_count, price, lifetime_hours
    except ValueError:
        return None