from enum import Enum


class TenderStatus(str, Enum):
    active    = "active"     # текущий активный тендер
    queued    = "queued"     # ожидает в очереди
    completed = "completed"  # завершён
