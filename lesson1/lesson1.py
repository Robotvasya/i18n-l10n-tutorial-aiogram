from aiogram import Bot, Dispatcher, F, html
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _


from aiogram.utils.i18n import lazy_gettext as __
from aiogram.utils.i18n import I18n, ConstI18nMiddleware

TOKEN = "TOKEN"
dp = Dispatcher()


@dp.message(F.text == __("Start"))
async def handler_1(message: Message) -> None:
    await message.answer(_("Welcome, {name}!").format(name=html.quote(message.from_user.full_name)))
    await message.answer(_("How many coins do you have? Input number, please:"))


@dp.message(F.text)
async def handler_2(message: Message) -> None:

    try:
        n = int(message.text)
        await message.answer(_("You have {} coin!", "You have {} coins!", n).format(n))
    except ValueError:
        await message.answer(_("Please, enter a number"))


def main() -> None:
    bot = Bot(TOKEN, parse_mode="HTML")
    i18n = I18n(path="locales", default_locale="en", domain="my-super-bot")
    dp.message.outer_middleware(ConstI18nMiddleware(locale='ru', i18n=i18n))
    dp.run_polling(bot)


if __name__ == "__main__":
    main()
