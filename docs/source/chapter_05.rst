Глава 5. Интернационализация в Aiogram с использованием Fluent.
---------------------------------------------------------------

Подготовка кода
~~~~~~~~~~~~~~~

Для хорошей поддержки интернационализации и локализации разработчики
Aiogram создали отдельный пакет ``aiogram_i18n`` `<https://github.com/aiogram/i18n>`_, в который добавили
поддержку движка локализации ``Fluent для Python`` https://github.com/projectfluent/python-fluent.

Установим его с помощью команды:

.. code-block:: bash

   pip install aiogram_i18n

Также нам потребуются ``FluentCompileCore`` и ``FluentRuntimeCore``

.. code-block:: bash

   pip install fluent_compiler

.. code-block:: bash

   pip install fluent.runtime

В предыдущем разделе мы рассказывали о том, что подход к созданию файлов
перевода у Fluent в корне отличается от привычного. По сути теперь
интернационализация полностью в ваших руках, а локализацию выполняет
ядро Python Fluent. У нас теперь нет шаблонов перевода и мы не извлекаем
строки из исходного кода нашего проекта. Хотя есть различные плагины для
IDE, которые могут нам помочь с извлечением строк. Отказ от
использования строк английского текста как ключей, накладывает некоторые
ограничения в угоду гибкости самих переводов. Теперь нам нужно самим
проектировать ПО так, чтобы перевод был возможен. И по-началу будет
много ручной работы. Проект Fluent - 2017 год, и по меркам gettext 1995
года, он еще молодой. Инструменты автоматизации, которые я нашел,
созданы в основном для JavaScript (в силу специфики разработки под
локализацию браузера Firefox). Поэтому пока будем создавать файлы
перевода вручную.

Создадим код нашего нового проекта:

.. code-block:: python
   :caption: lesson2.py
   :linenos:

   import asyncio
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
       ], resize_keyboard=True)

   @router.message(CommandStart())
   async def cmd_start(message: Message, i18n: I18nContext) -> Any:
       name = message.from_user.mention_html()
       return message.reply(
           text=i18n.get("hello", user=name),  # or i18n.hello(user=name)
           reply_markup=rkb)


   @router.message(F.text == LazyProxy("help"))
   async def cmd_help(message: Message) -> Any:
       return message.reply(text="-- " + message.text + " --")

   async def main() -> None:
       basicConfig(level=INFO)
       bot = Bot("TOKEN", parse_mode=ParseMode.HTML)
       i18n_middleware = I18nMiddleware(
           core=FluentRuntimeCore(
               path="locales/{locale}/LC_MESSAGES",
           ),
           default_locale="ru")
       dp = Dispatcher()
       dp.include_router(router)
       i18n_middleware.setup(dispatcher=dp)
       await dp.start_polling(bot)


   if __name__ == "__main__":
       asyncio.run(main())

Мы импортировали следующие объекты:

.. code-block:: python
   :lineno-start: 10


   from aiogram_i18n import I18nContext, LazyProxy, I18nMiddleware
   from aiogram_i18n.cores.fluent_runtime_core import FluentRuntimeCore
   from aiogram_i18n.types import (
       ReplyKeyboardMarkup, KeyboardButton
       # you should import mutable objects from here if you want to use LazyProxy in them
   )

Нам понадобится сам движок ``FluentRuntimeCore``, также контекст
``I18nContext`` и один из вариантов middleware (для примера я взял
``I18nMiddleware``). Также нужны нам ``LazyProxy`` - ленивые строки,
какие мы видели в ``lazy gettext``. И изменяемые объекты Aiogram, такие,
как клавиатура, которые нужно импортировать именно из
``aiogram_i18n.types``. Эти объекты нам нужны, когда работа с объектом
происходит, но язык еще не известен, так как код выполняется еще за
пределами роутеров. И перевод будет добавлен лениво, то есть в самом
конце перед передачей пользователю.

Создадим объект нашего middleware:

.. code-block:: python
   :lineno-start: 38

   i18n_middleware = I18nMiddleware(
           core=FluentRuntimeCore(
               path="locales/{locale}/LC_MESSAGES", # путь к папке локалей
               ),
           default_locale="ru") # язык интерфейса. Переключать научимся позже.

И зарегистрируем его через встроенный метод setup (в этом методе реализована регистрация компонентов в нужном порядке)

.. code-block:: python
   :lineno-start: 45

   i18n_middleware.setup(dispatcher=dp)

Создадим файл переводов в формате ``FTL`` (Fluent Translation List).

Файл следующего содержания с английским переводом ``my-super-bot.ftl`` положим в папку ``locales/en/LC_MESSAGES``:

.. code-block:: fluent
   :caption: locales/en/LC_MESSAGES/my-super-bot.ftl

   hello = Hello, <b>{ $user }</b>!
   cur-lang = Your current language: <i>{ $language }</i>
   help = Help

Файл с русским переводом ``my-super-bot.ftl`` положим в папку ``locales/ru/LC_MESSAGES``:

.. code-block:: fluent
   :caption: locales/ru/LC_MESSAGES/my-super-bot.ftl

   hello = Привет, <b>{ $user }</b>!
   cur-lang = Текущий язык : <i>{ $language }</i>
   help = Помощь

Запустим и проверим работу на русском языке. Затем изменим язык в middleware и проверим на английском:

.. code-block:: python
   :lineno-start: 38

   i18n_middleware = I18nMiddleware(
           core=FluentRuntimeCore(
               path="locales/{locale}/LC_MESSAGES", # путь к папке локалей
               ),
           default_locale="en")
