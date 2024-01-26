import asyncio
import logging
from logging import basicConfig, INFO
from typing import Any

from aiogram import Router, Dispatcher, F, Bot
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

from aiogram_i18n import I18nContext, LazyProxy, I18nMiddleware
from aiogram_i18n.cores.fluent_runtime_core import FluentRuntimeCore
from aiogram_i18n.types import (
    ReplyKeyboardMarkup, KeyboardButton
    # you should import mutable objects from here if you want to use LazyProxy in them
    )

router = Router(name=__name__)
rkb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=LazyProxy("help"))]  # or L.help()
    ], resize_keyboard=True
)


@router.message(CommandStart())
async def cmd_start(message: Message, i18n: I18nContext) -> Any:
    name = message.from_user.mention_html()
    return message.reply(
        text=i18n.hello(user=name), #i18n.get("hello", user=name),  # or i18n.hello(user=name)
        reply_markup=rkb
    )


@router.message(F.text == LazyProxy("help"))
async def cmd_help(message: Message) -> Any:
    return message.reply(text="-- " + message.text + " --")

@router.message(F.text)
async def handler_2(message: Message, i18n: I18nContext) -> None:
    try:
        name = message.from_user.mention_html()
        n = int(message.text)
        await message.answer(text=i18n.get("you-have-coin", value=n, user=name))
    except ValueError as e:
        logging.log(INFO, e)
        await message.answer(text=i18n.get("enter-a-number"))


async def main() -> None:
    basicConfig(level=INFO)
    bot = Bot("TOKEN", parse_mode=ParseMode.HTML)
    i18n_middleware = I18nMiddleware(
        core=FluentRuntimeCore(
            path="locales/{locale}/LC_MESSAGES",

        ),
        # locale_key="ru",
        default_locale="ru"
    )

    dp = Dispatcher()
    dp.include_router(router)
    i18n_middleware.setup(dispatcher=dp)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
