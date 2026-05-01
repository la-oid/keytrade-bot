from pathlib import Path

# ── Корень проекта (на уровень выше app/) ─────────────────────────────────────
ROOT = Path(__file__).parent.parent.parent  # keytrade-bot/

# ── Data (корень проекта) ─────────────────────────────────────────────────────
DATA_DIR             = ROOT / "data"
CRYPTO_NETWORKS_FILE = DATA_DIR / "crypto_networks.json"
IMAGES_DIR           = DATA_DIR / "images"

# ── Storage ───────────────────────────────────────────────────────────────────
STORAGE_DIR = ROOT / "storage"
PDF_DIR     = STORAGE_DIR / "pdf"


def ensure_dirs() -> None:
    """Создаёт все нужные директории если их нет."""
    for d in [DATA_DIR, IMAGES_DIR, PDF_DIR]:
        d.mkdir(parents=True, exist_ok=True)