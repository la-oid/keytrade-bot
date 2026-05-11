from datetime import datetime

from loguru import logger

from app.shared import db
from app.db import Database
from app.db.models.tender import Tender
from app.db.enums.tender import TenderStatus
from app.shared.constants import TENDER_DEFAULT_TOTAL, TENDER_MAX_PIE_KEYS


class TenderService:
    """Бизнес-логика тендеров."""

    def __init__(self, db: Database):
        self.db = db

    # ─── Инициализация ───────────────────────────────────────────────────────

    async def ensure_active(self) -> None:
        """При старте бота гарантирует наличие активного тендера."""
        active = await self.db.tender.get_active()
        if not active:
            tender = await self.db.tender.create(TENDER_DEFAULT_TOTAL, TenderStatus.active)
            logger.info(f"Tender: created default active {tender.id} ({TENDER_DEFAULT_TOTAL} keys)")

    # ─── Пополнение из паёв ──────────────────────────────────────────────────

    async def add_keys_from_order(self, amount: int) -> None:
        """Вызывается при подтверждении оплаты. Паи > TENDER_MAX_PIE_KEYS игнорируются."""
        if amount > TENDER_MAX_PIE_KEYS:
            return

        active = await self.db.tender.get_active()
        if not active:
            return

        updated = await self.db.tender.add_keys(active.id, amount)
        logger.debug(f"Tender {active.id}: +{amount} keys ({updated.current_keys}/{active.total_keys})")

        if updated.current_keys >= active.total_keys:
            await self._complete_and_launch_next(active.id)

    # ─── Ручные действия (admin) ─────────────────────────────────────────────

    async def add_manually(self, amount: int) -> Tender:
        """Ручное добавление к активному тендеру (без ограничения 500 шт)."""
        active = await self.db.tender.get_active()
        if not active:
            active = await self.db.tender.create(TENDER_DEFAULT_TOTAL, TenderStatus.active)

        updated = await self.db.tender.add_keys(active.id, amount)
        logger.info(f"Tender {active.id}: manual +{amount} ({updated.current_keys}/{active.total_keys})")

        if updated.current_keys >= active.total_keys:
            await self._complete_and_launch_next(active.id)
            active = await self.db.tender.get_active()
            return active

        return updated

    async def add_to_queue(self, total_keys: int) -> Tender:
        """Добавляет тендер в очередь."""
        tender = await self.db.tender.create(total_keys, TenderStatus.queued)
        logger.info(f"Tender {tender.id}: queued ({total_keys} keys)")
        return tender

    async def launch_now(self, total_keys: int) -> Tender:
        """Немедленно запускает новый тендер, завершая текущий."""
        active = await self.db.tender.get_active()
        if active:
            await self.db.tender.set_status(active.id, TenderStatus.completed, completed_at=datetime.utcnow())
            logger.info(f"Tender {active.id}: completed (launch_now)")

        tender = await self.db.tender.create(total_keys, TenderStatus.active)
        logger.info(f"Tender {tender.id}: launched now ({total_keys} keys)")
        return tender

    # ─── Статус ──────────────────────────────────────────────────────────────

    async def get_active(self) -> Tender | None:
        return await self.db.tender.get_active()

    async def notify_admins(self) -> None:
        """Отправляет статус активного тендера всем администраторам. Вызывается из scheduler."""
        from app.shared import bots
        from app.shared.config import settings

        tender = await self.db.tender.get_active()
        if not tender:
            return

        text = f"Тендер: <b>{tender.current_keys}/{tender.total_keys} шт</b>"
        for admin_id in settings.telegram.ADMIN_IDS:
            try:
                await bots.admin.bot.send_message(chat_id=admin_id, text=text)
            except Exception:
                pass

    # ─── Внутренняя логика ────────────────────────────────────────────────────

    async def _complete_and_launch_next(self, tender_id: int) -> None:
        """Завершает тендер и запускает следующий из очереди (или дефолтный)."""
        await self.db.tender.set_status(tender_id, TenderStatus.completed, completed_at=datetime.utcnow())
        logger.info(f"Tender {tender_id}: completed")

        next_tender = await self.db.tender.get_next_queued()
        if next_tender:
            await self.db.tender.set_status(next_tender.id, TenderStatus.active)
            logger.info(f"Tender {next_tender.id}: activated from queue")
        else:
            new = await self.db.tender.create(TENDER_DEFAULT_TOTAL, TenderStatus.active)
            logger.info(f"Tender {new.id}: default active created ({TENDER_DEFAULT_TOTAL} keys)")


tender_service = TenderService(db)
