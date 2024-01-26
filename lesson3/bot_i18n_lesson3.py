import asyncio
import logging
from logging import basicConfig, INFO
from typing import Any

from aiogram import Router, Dispatcher, F, Bot
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile

from aiogram_i18n import I18nContext, LazyProxy, I18nMiddleware
from aiogram_i18n.cores.fluent_runtime_core import FluentRuntimeCore
from aiogram_i18n.types import (
    ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
    # you should import mutable objects from here if you want to use LazyProxy in them
)

from database import database
from database.database import Database
from middlewares import db_middleware
from middlewares import i18n_middleware

router = Router(name=__name__)

rkb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=LazyProxy("help", case="capital"))]  # or L.help()
    ], resize_keyboard=True
)


@router.message(CommandStart())
async def process_start_command(message: Message, i18n: I18nContext, db: Database):
    if not db.get_user(message.from_user.id):
        db.add_user(message.from_user.id, message.from_user.username)
    name = message.from_user.full_name

    await message.answer(text=i18n.hello(user=name, language=i18n.locale),# text=i18n.get("hello", user=name))
                         reply_markup=rkb
                         )


@router.message(Command("help"))
@router.message(F.text == LazyProxy("help", case="capital"))
@router.message(F.text == LazyProxy("help", case="lower"))
async def cmd_help(message: Message, i18n: I18nContext) -> Any:
    return message.reply(text=i18n.get("help-message"))


async def switch_language(message: Message, i18n: I18nContext, locale_code: str):
    await i18n.set_locale(locale_code)
    await message.answer(i18n.get("lang-is-switched"), reply_markup=rkb)


@router.message(Command("language_en"))
async def switch_to_en(message: Message, i18n: I18nContext) -> None:
    await switch_language(message, i18n,"en")


@router.message(Command("language_ru"))
async def switch_to_en(message: Message, i18n: I18nContext) -> None:
    await switch_language(message, i18n,"ru")


@router.message(Command("photo"))
@router.message(F.text == LazyProxy("photo"))
async def sent_photo(message: Message, i18n: I18nContext) -> None:
    locale_code = i18n.locale
    path_to_photo = f"locales/{locale_code}/static/bayan_{locale_code}.jpg"

    await message.answer_photo(photo=FSInputFile(path_to_photo))


@router.message()
async def handler_common(message: Message, i18n: I18nContext) -> None:
    await message.answer(text=i18n.get("i-dont-know"))
    await message.answer(text=i18n.get("show-date", date_=message.date))


async def main() -> None:
    basicConfig(level=INFO)
    bot = Bot("TOKEN", parse_mode=ParseMode.HTML)

    dp = Dispatcher()
    dp.include_router(router)

    # создаем объект middleware пакета локализации aiogram_i18n
    i18n = I18nMiddleware(
        core=FluentRuntimeCore(
            path="locales/{locale}/LC_MESSAGES",
            # path="locales/{locale}"
        ),
        # передаем наш кастомный менеджер языка из middlewares/i18n_middleware.py
        manager=i18n_middleware.UserManager(),
        # locale_key="ru",
        default_locale="en"
    )

    # Регистрация мидлварей. Сначала регистрируется база данных, так как там хранится язык.
    dp.update.outer_middleware.register(db_middleware.DBMiddleware())
    i18n.setup(dispatcher=dp)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())


# Домашка:
# Перевести всплывающую подсказку, кнопку в закрепе и меню бота.
# Исправить работу вывода даты в ответах бота. Не выводится день недели и месяц в неправильном формате.
# Написать код, который проверяет пол (из бд), вслучае необходимости запрашивает у пользователя и формирует
# в человеческий вид сообщение на двух языках:
# Ты, %username% мог(ла) бы чаще улыбаться!
#   и
# Его (её, их) фото пора в сториз.
# Написать кэширование к выбору языка, например хранение в сторадже redis.
