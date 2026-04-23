class BaseInlineKeyboard:
    """Базовый класс для inline-клавиатур."""

    def __init__(self):
        from ...texts import ButtonTexts
        self.texts = ButtonTexts