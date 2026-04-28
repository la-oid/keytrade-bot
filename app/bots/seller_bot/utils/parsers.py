def parse_keys_file(content: str) -> list[str] | None:
    """
    Парсит содержимое .txt файла со списком ключей.
    Один ключ на строку, пустые строки игнорируются.
    Возвращает список ключей или None если ничего не найдено.
    """
    keys = [line.strip() for line in content.splitlines() if line.strip()]
    return keys or None