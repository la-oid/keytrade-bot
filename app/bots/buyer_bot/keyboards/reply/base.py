class BaseReplyKeyboard:
    """Базовый класс для reply-клавиатур."""

    def __init__(self):
        from ...texts import ButtonTexts
        self.texts = ButtonTexts