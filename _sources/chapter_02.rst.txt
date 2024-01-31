Глава 2. Интернационализация в Aiogram утилитами GNU gettext.
-------------------------------------------------------------

Подготовка кода.
~~~~~~~~~~~~~~~~~

Во фреймворке Aiogram предусмотрена возможность использования
интернационализации (https://docs.aiogram.dev/en/latest/utils/i18n.html)
с помощью библиотеки GNU gettext
(https://docs.python.org/3/library/gettext.html) и инструментов Babel
(https://babel.pocoo.org/en/latest/).

Установка пакета для переводов происходит через дополнительную
зависимость командой

.. code-block:: bash

   pip install aiogram[i18n]

Либо можно непосредственно установить сам Babel

.. code-block:: bash

   pip install Babel

Первый и важный шаг для работы по интернационализации — нам нужно
подготовить наш код таким образом, чтобы он смог использовать файлы
перевода и загружать необходимые фразы из нужной локали. Для этого все
переводимые строки необходимо обернуть функцией gettext. Функцию
подстановки перевода из gettext принято обозначать ``_`` - одинарное
нижнее подчеркивание, а вызов этой функции ``_()``.

.. code-block:: python

   from aiogram import html
   from aiogram.utils.i18n import gettext as _
   # импортируем модуль gettext из aiogram utils как _

Обертываем все строки, которые нуждаются в переводе функцией gettext.

Было:

.. code-block:: python

   async def my_handler(message: Message) -> None:
       await message.answer(f"Hello, {html.quote(message.from_user.full_name)}!")

Стало:

.. code-block:: python

   async def my_handler(message: Message) -> None:
       await message.answer(_("Hello, {name}!").format(name=html.quote(message.from_user.full_name)))

.. attention::
   Обратите внимание, что Gettext **не может использовать f-строки**. Поскольку при
   использовании f-строк нельзя сначала создать шаблон, а затем его
   использовать. Это происходит из-за того, что f-строка сразу выполняется
   и в нее подставляются значения переменных, которые должны быть
   определены ранее. А у нас сначала должен произойти перевод с
   подстановкой в шаблон строки. Поэтому нужно использовать метод строк
   ``format()``.

Более того, когда нам необходимо использовать перевод в фильтрах
ключевых слов или магических фильтрах, то нужно будет использовать
ленивые вызовы gettext - ``lazy_gettext``, которые будут обозначены
``__`` - двойное подчеркивание, а вызов этой функции ``__()``.

.. code-block:: python
   :emphasize-lines: 2

   from aiogram import F
   from aiogram.utils.i18n import lazy_gettext as __
   # Выше мы импортируем функцию ленивого вызова gettext как _ _



В документации особо обращено внимание на то, что ленивые вызовы
``lazy gettext`` всегда следует использовать, если текущий язык в данный
момент неизвестен.

Также важно, что ``lazy gettext`` нельзя использовать в качестве
значения для методов API или любого объекта Telegram (например, для
aiogram.types.inline_keyboard_button.InlineKeyboardButton и т. д.).

.. _`Конфигурация-движка-перевода`:

Конфигурация движка перевода
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Сначала в коде проекта мы создаем объект класса ``I18n``, чтобы было
понятно, какой язык будет использоваться:

.. code-block:: python

   i18n = I18n(path="locales", default_locale="en", domain="my-super-bot")

Здесь:

``path=`` путь к папкам с локалями. В данном случае путь будет
сформирован будет так:
``locales/{language}/LC_MESSAGES/файл_перевода.mo``, а мы указываем
верхний уровень locales, исходя из нашей структуры:

::

   ...
   locales
   ├── messages.pot
   ├── en
   │   └── LC_MESSAGES
   │       └── my-super-bot.mo
   ├── ru
   │   └── LC_MESSAGES
   │       └── my-super-bot.mo
   ...

``default_locale=`` локаль по умолчанию, английская "en".

``domain=`` домен - это название домена переводов в gettext, по сути это
название приложения, для которого будет создана локаль (используется
чаще название того приложения, что мы переводим). Мы назвали
"my-super-bot".

**Движок перевода** - это middleware для I18n. И теперь нам необходимо
выбрать движок перевода, основанный на 4-х встроенных в aiogram классах
middleware из ``aiogram.utils.i18n.middleware``:

1. **SimpleI18nMiddleware** - выбирает код языка из объекта User,
   полученного в событии. Однако не все клиенты Telegram отдают это
   значение. Очень часто объект language_code не заполнен и является
   пустой строкой.
2. **ConstI18nMiddleware** - выбирает статически определенную локаль.
3. **FSMI18nMiddleware** - хранит локаль в хранилище FSM.
4. **I18nMiddleware** - это базовый абстрактный класс для наследования и
   создания собственного обработчика.

Наш код будет выглядеть примерно так:

.. code-block:: python
   :linenos:

   from aiogram import Bot, Dispatcher, F
   from aiogram.types import Message

   from aiogram.utils.i18n import gettext as _
   from aiogram.utils.i18n import lazy_gettext as __
   from aiogram.utils.i18n import I18n, ConstI18nMiddleware

   TOKEN = "token"
   dp = Dispatcher()

   @dp.message(F.text == __('Test'))
   async def test1(message: Message) -> None:
       await message.answer(_("Hello, {name}!").format(name=html.quote(message.from_user.full_name)))

   def main() -> None:
       bot = Bot(TOKEN, parse_mode="HTML")
       i18n = I18n(path="locales", default_locale="en", domain="my-super-bot")
       dp.message.outer_middleware(ConstI18nMiddleware(locale='en', i18n=i18n))

       dp.run_polling(bot)

   if __name__ == "__main__":
       main()
