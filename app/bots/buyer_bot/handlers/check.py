from pathlib import Path
from datetime import datetime
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.types import FSInputFile

from app.shared import db, bots, settings
from app.shared.paths import PDF_DIR
from app.db.enums import PaymentStatus
from ..utils import notify_admins
from ..texts import Texts
from ..keyboards import InlineKeyboards

r = Router()

texts = Texts()
buttons = InlineKeyboards()

# Папка для PDF
storage = Path(PDF_DIR)
storage.mkdir(parents=True, exist_ok=True)


@r.callback_query(F.data == "payment_sent")
async def payment_sent_handler(call: CallbackQuery, user):
    """Нажал 'Перевёл' → переводим в PENDING_PDF и просим квитанцию."""

    # Проверяем что пользователь на этапе ожидания оплаты
    payment = await db.payment.get_by_status(user.telegram_id, PaymentStatus.PENDING_PAY)
    if not payment:
        await call.answer()
        return

    # Переводим платёж на этап ожидания PDF
    await db.payment.set_status(payment.id, PaymentStatus.PENDING_PDF)

    # Показываем пользователю экран ожидания квитанции
    await call.answer()
    await call.message.edit_text(texts.payment.WAITING_PDF)


@r.message(F.document)
async def receive_pdf_handler(msg: Message, user):
    """Приём PDF-квитанции → сохраняем в storage/pdfs и переводим в PENDING_REVIEW."""

    # Проверяем что пользователь на этапе ожидания PDF
    payment = await db.payment.get_by_status(user.telegram_id, PaymentStatus.PENDING_PDF)
    if not payment:
        return

    # Проверяем формат
    if msg.document.mime_type != "application/pdf":
        await msg.answer(texts.payment.WRONG_FORMAT)
        return

    # Формируем имя: payment_id + telegram_id + timestamp
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    filename = f"payment_{payment.id}_user_{user.telegram_id}_{timestamp}.pdf"
    path = storage / filename

    # Скачиваем файл из Telegram на диск
    await bots.buyer.bot.download(msg.document, destination=path)

    # Сохраняем путь в БД и переводим в PENDING_REVIEW
    await db.payment.set_pdf_path(payment.id, str(path))

    # Возвращаем покупателя на экран "Мои заказы"
    await msg.answer(
        texts.profile.ORDERS_LIST,
        reply_markup=await buttons.profile.orders_list(user.telegram_id),
    )

    # Уведомляем админов: текст + сам PDF-файл
    pdf_file = FSInputFile(path)
    caption = texts.payment.ADMIN_PDF_RECEIVED.format(
        name=user.first_name or user.username,
        user_id=user.telegram_id,
        bank=payment.bank,
        price=payment.price,
        amount=payment.amount,
        payment_id=payment.id,
    )

    # Уведомляем админов
    await notify_admins(caption, document=pdf_file)