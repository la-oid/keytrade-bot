import json

from curl_cffi.requests import AsyncSession
from loguru import logger

from app.shared.paths import COOKIES_FILE
from app.shared.constants import CARDLINK_BASE_URL, MARKET_BILLER


GRAPHQL_URL = "https://market.csgo.com/api/graphql?lang=en"

CREATE_CHECKIN_MUTATION = """
mutation createCheckinRequest($amount: Float!, $biller: String!, $extra_data: String, $payout_currency: String, $wallet: String) {
  createCheckinRequest(amount: $amount, biller: $biller, extra_data: $extra_data, payout_currency: $payout_currency, wallet: $wallet) {
    invoice_id
    code
    message
    redirect
    qr
    qr_ttl
    success
  }
}
""".strip()


class PaymentSessionDead(Exception):
    """Cookies в cookie.json протухли — нужно обновить файл вручную."""


class PaymentAPIError(Exception):
    """Market API вернул ошибку (лимит, биллер недоступен, антифрод)."""


def _load_session() -> tuple[dict, str]:
    """Читает cookie.json и возвращает (cookies dict, user_agent)."""
    if not COOKIES_FILE.exists():
        raise RuntimeError(
            f"Файл {COOKIES_FILE} не найден. "
            f"Создай его по образцу из README."
        )

    with open(COOKIES_FILE, "r", encoding="utf-8") as f:
        raw = json.load(f)

    user_agent = raw.get("user_agent", "")
    cookies_raw = raw.get("cookies", [])
    cookies = {c["name"]: c["value"] for c in cookies_raw if "name" in c}

    return cookies, user_agent


class PaymentService:
    """Создание платёжных ссылок через market.csgo.com."""

    async def create_invoice(self, amount: float) -> str:
        """
        Создаёт invoice на указанную сумму и возвращает invoice_id.

        Raises:
            PaymentSessionDead: cookie.json протухли, нужно обновить
            PaymentAPIError: market отказал (лимит, недоступен биллер и т.д.)
        """
        invoice_id = await self._create_invoice(amount)
        invoice_id = str(invoice_id)
        logger.info(f"Payment: created invoice {invoice_id} for {amount}₽")
        return invoice_id

    async def _create_invoice(self, amount: float) -> int:
        """Делает GraphQL-запрос и возвращает invoice_id."""
        cookies, ua = _load_session()

        payload = {
            "operationName": "createCheckinRequest",
            "variables": {
                "amount": float(amount),
                "biller": MARKET_BILLER,
                "extra_data": "{}",
                "wallet": None,
                "payout_currency": None,
            },
            "query": CREATE_CHECKIN_MUTATION,
        }

        async with AsyncSession(impersonate="chrome120") as s:
            s.cookies.update(cookies)
            r = await s.post(
                GRAPHQL_URL,
                json=payload,
                headers={
                    "User-Agent": ua,
                    "Accept": "application/json, text/plain, */*",
                    "Accept-Language": "ru-RU,ru;q=0.9",
                    "Content-Type": "application/json",
                    "App-Settings": "lang=en",
                    "Referer": "https://market.csgo.com/en/usercab/balance",
                    "Origin": "https://market.csgo.com",
                },
                timeout=20,
            )

        return self._parse_response(r)

    def _parse_response(self, r) -> int:
        """Парсит ответ market и возвращает invoice_id. Кидает исключение при ошибке."""
        content_type = r.headers.get("content-type", "")
        if "text/html" in content_type:
            raise PaymentSessionDead(
                f"Cloudflare блок (HTTP {r.status_code}) — нужен свежий cookie.json"
            )

        if r.status_code in (401, 403):
            raise PaymentSessionDead(f"HTTP {r.status_code} — cookies протухли")

        if r.status_code != 200:
            raise PaymentAPIError(f"HTTP {r.status_code}: {r.text[:300]}")

        try:
            body = r.json()
        except Exception as e:
            raise PaymentAPIError(f"Невалидный JSON: {e} | body={r.text[:300]}")

        if "errors" in body:
            errors_text = json.dumps(body["errors"], ensure_ascii=False)
            if "auth" in errors_text.lower() or "unauthenticated" in errors_text.lower():
                raise PaymentSessionDead(f"GraphQL: {errors_text}")
            raise PaymentAPIError(f"GraphQL errors: {errors_text}")

        res = body.get("data", {}).get("createCheckinRequest")
        if not res:
            raise PaymentAPIError(f"Неожиданный ответ: {body}")

        if not res.get("success"):
            raise PaymentAPIError(
                f"Отказ: code={res.get('code')} message={res.get('message')}"
            )

        return res["invoice_id"]


payment_service = PaymentService()
