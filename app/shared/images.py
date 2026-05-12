from app.shared.paths import IMAGES_DIR


class BuyerImages:
    """Пути к картинкам buyer_bot."""
    START            = IMAGES_DIR / "buyer" / "start.png"
    PROFILE          = IMAGES_DIR / "buyer" / "profile.png"
    MEDIUM_WHOLESALE = IMAGES_DIR / "buyer" / "medium_wholesale.png"
    LARGE_WHOLESALE  = IMAGES_DIR / "buyer" / "large_wholesale.png"
    ORDER_PENDING    = IMAGES_DIR / "buyer" / "order_pending.png"


class SellerImages:
    """Пути к картинкам seller_bot."""
    START           = IMAGES_DIR / "seller" / "start.png"
    PROFILE         = IMAGES_DIR / "seller" / "profile.png"
    ORDERS          = IMAGES_DIR / "seller" / "orders.png"
    PAYMENT_CREATED = IMAGES_DIR / "seller" / "payment_created.png"
    KEYS_ACCEPTED   = IMAGES_DIR / "seller" / "keys_accepted.png"