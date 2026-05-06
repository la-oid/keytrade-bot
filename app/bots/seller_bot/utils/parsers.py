from aiogram.types import Message, Document


def parse_keys_file(content: str) -> list[str] | None:
    """Парсит .txt файл — один ключ на строку. Возвращает список или None"""
    return [line.strip() for line in content.splitlines() if line.strip()] or None 


def is_text_file(doc: Document) -> bool:
    """Проверяет что документ является текстовым файлом (.txt или mime text/plain)."""
    file_name = doc.file_name or ""
    return file_name.lower().endswith(".txt") or doc.mime_type == "text/plain"
 
 
async def download_text_file(msg: Message) -> str:
    """Скачивает документ и возвращает содержимое как строку."""
    file   = await msg.bot.get_file(msg.document.file_id)
    buffer = await msg.bot.download_file(file.file_path)
    return buffer.read().decode("utf-8", errors="ignore")