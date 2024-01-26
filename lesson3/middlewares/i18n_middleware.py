from aiogram_i18n.managers import BaseManager
from aiogram.types.user import User
from database.database import Database


class UserManager(BaseManager):
    """Собственная реализация middleware для интернационализации
    на базе класса BaseManager из библиотеки aiogram_i18n.
    BaseManager имеет абстрактные методы set_locale и get_locale, которые
    нам нужно реализовать. Кроме того, при инициализации объекта класса,
    выполняются LocaleSetter и LocaleGetter (см. реализацию BaseManager).

    В случае использования gettext необходимо проверить реализацию
    класса, так как не gettext не тестировалось
    """
    async def get_locale(self, event_from_user: User, db: Database = None) -> str:
        default = event_from_user.language_code or self.default_locale
        if db:
            user_lang = db.get_lang(event_from_user.id)
            if user_lang:
                return user_lang
        return default


    async def set_locale(self, locale: str, event_from_user: User, db: Database = None) -> None:
        if db:
            db.set_lang(event_from_user.id, locale)
