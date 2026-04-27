class MenuTexts:
    """Тексты меню"""
 
    START_TEXT = (
        "Добрый день! Вас приветствует бот-агрегатор.\n\n"
        "Выберите раздел из меню снизу."
    )
 
    PROFILE_TEXT = "Профиль скоро будет доступен."
 
    MARKET_TEXT = "Площадка заказов скоро будет доступна."
 
    ABOUT_TEXT = (
        "Мы — агрегаторная платформа, которая помогает продавцам "
        "сдавать ключи в выгодные паи и получать стабильный доход.\n\n"
        "Подробнее о нас и условиях работы скоро здесь."
    )
 
    SUPPORT_TEXT = "Если у вас вопрос или проблема — напишите в поддержку: {url}"


class ProfileTexts:
    """Тексты профиля"""
 
    pass


class MarketTexts:
    """Тексты площадки заказов"""
 
    pass


class MiscTexts:
    """Общие тексты"""
    
    pass


class Texts:
    """Все тексты"""
    menu = MenuTexts
    profile = ProfileTexts
    market  = MarketTexts
    misc = MiscTexts