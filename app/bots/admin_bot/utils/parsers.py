def parse_order_create(text: str) -> tuple[int, int] | None:
    """
    Парсит строку вида 'кол-во, часы'.
    Возвращает (keys_count, lifetime_hours) или None при ошибке.
    """
    parts = text.strip().replace(" ", "").split(",")

    if len(parts) != 2:
        return None

    try:
        keys_count     = int(parts[0])
        lifetime_hours = int(parts[1])

        if keys_count <= 0 or lifetime_hours <= 0:
            return None

        return keys_count, lifetime_hours
    except ValueError:
        return None