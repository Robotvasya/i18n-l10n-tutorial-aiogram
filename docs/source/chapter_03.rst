Глава 3. Локализация Aiogram, создание переводов и работа с Babel.
------------------------------------------------------------------

Шаблоны переводов
~~~~~~~~~~~~~~~~~

Переходим ко второму шагу к локализации. Теперь нам необходимо создать
сами переводы, основываясь на переменных, которые уже есть в нашем коде
и создать папки по такой структуре.

::

   ...
   locales
   ├── messages.pot
   ├── en
   │   └── LC_MESSAGES
   │       └── my-super-bot.po
   ├── ru
   │   └── LC_MESSAGES
   │       └── my-super-bot.po
   ...

Предварительно нужно только создать папку locales в корне проекта.
Остальная структура создается автоматически с помощью ранее
установленного пакета утилит Babel.

Создаем основу — шаблон переводов. Запускаем в корне проекта из
командной строки команду:

.. code-block:: bash

   pybabel extract --input-dirs=. -o locales/messages.pot

Утилита проходит по нашим файлам и извлекает все строковые переменные,
обернутые функциями ``_()`` и ``__()``, в файл шаблона messages.pot.

У нас получится файл ``.pot`` (Portable Object Template, а в
простонародье горшок) — это шаблон переводов, на основании которого
генерируются переводы:

.. code-block:: pot
   :caption: locales/messages.pot
   :emphasize-lines: 1, 2, 10-11

   # Translations template for Bot Super Project.
   # Copyright (C) 2024 John Doe
   # This file is distributed under the same license as the Bot Super Project
   # project.
   # FIRST AUTHOR <EMAIL@ADDRESS>, 2024.
   #
   #, fuzzy
   msgid ""
   msgstr ""
   "Project-Id-Version: Bot Super Project 0.1\n"
   "Report-Msgid-Bugs-To: john@doe-email.com\n"
   "POT-Creation-Date: 2024-01-12 16:11+0500\n"
   "PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE\n"
   "Last-Translator: FULL NAME <EMAIL@ADDRESS>\n"
   "Language-Team: LANGUAGE <LL@li.org>\n"
   "MIME-Version: 1.0\n"
   "Content-Type: text/plain; charset=utf-8\n"
   "Content-Transfer-Encoding: 8bit\n"
   "Generated-By: Babel 2.13.1\n"

   #: lesson1.py:13
   msgid "Hello, {name}!"
   msgstr ""

Обратите внимание, что при работе с gettext и Babel комментари,
начинающиеся с ``#``, являются значимыми — то есть их нельзя удалять.

Файл мы заполним своими данными (выделенные строки): это название проекта,
версия, копирайты и электронный адрес для связи в случае багов. По идее
это можно сразу сделать из командной строке при формировании шаблона
переводов:

.. code-block:: bash

   pybabel extract -o locales/messages.pot --copyright-holder="John Doe" --project="Bot Super Project" --version=0.1 --msgid-bugs-address=john@doe-email.com --input-dirs=.

Шаблон генерируется каждый раз после исправления или доработки кода,
поэтому мы не храним его в репозитории исходников git. На основании
шаблона будут создаваться файлы переводов на нужные нам языки.

Давайте создадим файл перевода на английский язык. Выполним в командной
строке:

.. code-block:: bash

   pybabel init -i locales/messages.pot -d locales -D my-super-bot -l en

А затем на русский:

.. code-block:: bash

   pybabel init -i locales/messages.pot -d locales -D my-super-bot -l ru

Где,

``-i locales/messages.pot`` - путь к нашему шаблону .pot

``-d locales`` - наш каталог переводов

``-D my-super-bot`` - наш домен переводов

``-l en`` — код языка.

Будет создан файл перевода ``my-super-bot.po`` в папке ``locales/en/LC_MESSAGES/`` и ``locales/ru/LC_MESSAGES/``.

Файлы переводов .po
~~~~~~~~~~~~~~~~~~~

Файлы в формате ``.po`` предназначены для переводчиков. И храним мы их в
репозитории в development ветке. Они нам нужны на случай изменения или
добавления строк в проекте. Генерация новых ``.po`` файлов происходит с
учетом старых. Об этом чуть позже. Сначала откроем созданные файлы и
отредактируем их.

Нас интересуют строки вида

.. code-block:: po

   #: lesson1.py:13
   msgid "Hello, {name}!"
   msgstr ""

В комментарии указан файл, откуда взялась текстовая строка и номер
строки в этом файле. Затем идентификатор ``msgid`` и перевод ``msgstr``,
который будет подставлен пользователю с выбранным языком. Заполняем
перевод ``msgstr`` в обоих локалях ru и en.

Для ru

.. code-block:: po

   #: lesson1.py:13
   msgid "Hello, {name}!"
   msgstr "Привет, {name}!"

Для en

.. code-block:: po

   #: lesson1.py:13
   msgid "Hello, {name}!"
   msgstr "Hello, {name}!"

Теперь пользователь у которого язык английский, получит английское
сообщение, а русский — русское. Естественно какой у пользователя язык,
мы должны считать через наш middleware i18n.

Затем обязательно компилируем переводы в формат ``.mo`` и готово:

::

   pybabel compile -d locales -D my-super-bot

Внесение изменений в файлы переводов .po
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Разберем еще один момент, связанный с изменениями переводов.

В какой-то момент мы решили изменить логику бота. И изменили код
программы, изменив старые строки и добавив новые. Естественно мы вносим
изменения в код в парадигме интернационализации.

.. code-block:: python
   :caption: lesson1.py
   :linenos:
   :emphasize-lines: 15, 16, 20

   from aiogram import Bot, Dispatcher, F, html
   from aiogram.types import Message

   from aiogram.utils.i18n import gettext as _
   from aiogram.utils.i18n import lazy_gettext as __
   from aiogram.utils.i18n import I18n, ConstI18nMiddleware


   TOKEN = "token"
   dp = Dispatcher()


   @dp.message(F.text == __('start'))
   async def handler_1(message: Message) -> None:
       await message.answer(_("Welcome, {name}!").format(name=html.quote(message.from_user.full_name)))
       await message.answer(_("How many coins do you have? Input number, please:"))

   @dp.message(F.text)
   async def handler_2(message: Message) -> None:
       await message.answer(_("You have {} coins!").format(message.text))


   def main() -> None:
       bot = Bot(TOKEN, parse_mode="HTML")
       i18n = I18n(path="locales", default_locale="en", domain="my-super-bot")
       dp.message.outer_middleware(ConstI18nMiddleware(locale='en', i18n=i18n))
       dp.run_polling(bot)


   if __name__ == "__main__":
       main()

Мы добавили вопрос к пользователю и переделали приветственное сообщение.

Теперь нам снова нужно извлечь строки. Формируем ``.pot`` файл. Для
удобства в версию добавляем минорный релиз 0.1.1.

.. code-block:: bash

   pybabel extract -o locales/messages.pot --copyright-holder="John Doe" --project="Bot Super Project" —version=0.1.1 --msgid-bugs-address=john@doe-email.com —input-dirs=.

И получаем новый шаблон:

.. code-block:: pot
   :caption: locales/messages.pot
   :linenos:
   :emphasize-lines: 21-22, 25-26,29-30

   # Translations template for Bot Super Project.
   # Copyright (C) 2024 John Doe
   # This file is distributed under the same license as the Bot Super Project
   # project.
   # FIRST AUTHOR <EMAIL@ADDRESS>, 2024.
   #
   #, fuzzy
   msgid ""
   msgstr ""
   "Project-Id-Version: Bot Super Project 0.1.1\n"
   "Report-Msgid-Bugs-To: john@doe-email.com\n"
   "POT-Creation-Date: 2024-01-12 17:25+0500\n"
   "PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE\n"
   "Last-Translator: FULL NAME <EMAIL@ADDRESS>\n"
   "Language-Team: LANGUAGE <LL@li.org>\n"
   "MIME-Version: 1.0\n"
   "Content-Type: text/plain; charset=utf-8\n"
   "Content-Transfer-Encoding: 8bit\n"
   "Generated-By: Babel 2.13.1\n"

   #: lesson1.py:15
   msgid "Welcome, {name}!"
   msgstr ""

   #: lesson1.py:16
   msgid "How many coins do you have? Input number, please:"
   msgstr ""

   #: lesson1.py:20
   msgid "You have {} coins!"
   msgstr ""

Обновляем файлы переводов командой update.

.. code-block:: bash

   pybabel update -i locales/messages.pot -d locales -D my-super-bot -l ru

.. code-block:: bash

   pybabel update -i locales/messages.pot -d locales -D my-super-bot -l en

И мы видим следующую картину.

.. code-block:: po
   :caption: locales/ru/LC_MESSAGES/my-super-bot.po
   :linenos:
   :emphasize-lines: 24-26

   # Russian translations for Bot Super Project.
   # Copyright (C) 2024 John Doe
   # This file is distributed under the same license as the Bot Super Project
   # project.
   # FIRST AUTHOR <EMAIL@ADDRESS>, 2024.
   #
   msgid ""
   msgstr ""
   "Project-Id-Version: Bot Super Project 0.1\n"
   "Report-Msgid-Bugs-To: john@doe-email.com\n"
   "POT-Creation-Date: 2024-01-12 17:28+0500\n"
   "PO-Revision-Date: 2024-01-12 16:16+0500\n"
   "Last-Translator: FULL NAME <EMAIL@ADDRESS>\n"
   "Language: ru\n"
   "Language-Team: ru <LL@li.org>\n"
   "Plural-Forms: nplurals=3; plural=(n%10==1 && n%100!=11 ? 0 : n%10>=2 && "
   "n%10<=4 && (n%100<10 || n%100>=20) ? 1 : 2);\n"
   "MIME-Version: 1.0\n"
   "Content-Type: text/plain; charset=utf-8\n"
   "Content-Transfer-Encoding: 8bit\n"
   "Generated-By: Babel 2.13.1\n"

   #: lesson1.py:15
   #, fuzzy
   msgid "Welcome, {name}!"
   msgstr "Привет, {name}!"

   #: lesson1.py:16
   msgid "How many coins do you have? Input number, please:"
   msgstr ""

   #: lesson1.py:20
   msgid "You have {} coins!"
   msgstr ""

Прежний перевод сохранился, но при этом у нас строка была изменена с
Hello на Welcome.

Babel увидел это, сохранил нам строку, но пометил перевод коментарием
``#, fuzzy`` что обозначает нечеткий или неточный перевод. Если скомпилировать сразу,
то такая строка не будет переводиться и отображаться пользователю.

Нам нужно поправить текст и убрать эту метку ``fuzzy``.

.. code-block:: po
   :caption: locales/ru/LC_MESSAGES/my-super-bot.po
   :lineno-start: 23

   #: lesson1.py:15
   msgid "Welcome, {name}!"
   msgstr "Добро пожаловать, {name}!"

   #: lesson1.py:16
   msgid "How many coins do you have? Input number, please:"
   msgstr "Сколько у тебя монет? Введи число, пожайлуйста:"

   #: lesson1.py:20
   msgid "You have {} coins!"
   msgstr "У тебя {} монет!"

То же самое делаем со вторым языком, и снова компилируем переводы.

В результате у нас все хорошо, кроме такого момента.

Если мы введем 1, то бот ответит *"У тебя 1 монет!"* или *"You have 1 coins!"*,
что с точки зрения грамматики любого языка — неверно.

Множественные формы
~~~~~~~~~~~~~~~~~~~

Например, в русском языке используются несколько множественных форм: 1 монета 2, 3 или 4 монет, 11 монет.
А если слово сообщения, то 1 сообщение, 2 сообщения, 10 сообщений. И в английском у нас тоже проблема
со множественными числами — 1 coins, хотя ожидалось 1 coin, 2 coins.

Давайте победим и эту историю.

Помните, я говорил о значащих комментариях в файлах ``.pot`` и ``.po``.
В частности в файле переводов ``.po`` для каждого языка формируется формула,
которая определяет количество множественных форм и правила их формирования.
Тут и будет вся магия работы с переводами множественных форм. Она содержится в строчках:

.. code-block:: po
   :caption: locales/ru/LC_MESSAGES/my-super-bot.po
   :lineno-start: 16

   "Plural-Forms: nplurals=3; plural=(n%10==1 && n%100!=11 ? 0 : n%10>=2 && "
   "n%10<=4 && (n%100<10 || n%100>=20) ? 1 : 2);\n"

Это формула, по которой определяется для конкретного языка форма слова во множественном числе.
Формулу разберем потом. А для начала нам нужно вернуться к интернационализации нашего кода.

Функция gettext не умеет работать со множественными формами. Для этого
существует `ngettext <https://docs.python.org/3/library/gettext.html#gettext.ngettext>`_ из стандартной библиотеки python.
Однако для удобства в Aiogram это уже все спрятано в функции ``gettext`` из ``aiogram.utils.i18n``.

Добавляем два идентификатора: передаем фразу в единственном, затем во множественном числе, и аргумент, принимающий число.
Не забываем привести принимаемый от пользователя текст к int.

Изменим наш код.

.. code-block:: python
   :caption: lesson1.py
   :lineno-start: 18

   @dp.message(F.text)
   async def handler_2(message: Message) -> None:
       try:
           n = int(message.text)
           await message.answer(_("You have {} coin!", "You have {} coins!", n).format(n))
       except:
           await message.answer(_("Please, enter a number"))

Теперь снова нужно произвести извлечение строк с помощью Babel. Для
извлечения строк с разным количеством аргументов, нам нужно запускать
pybabel extract с опциями ``-k _:1,1t`` ``-k _:1,2`` для gettext и
``-k __`` для lazy gettext (два подчеркивания).

.. code-block:: bash

   pybabel extract -o locales/messages.pot -k _:1,1t -k _:1,2 -k __ \
   --copyright-holder="John Doe" \
   --project="Bot Super Project" \
   --version=0.1.1 --msgid-bugs-address=john@doe-email.com \
   --input-dirs=.

Babel может неадекватно извлекать строки, поэтому можно воспользоваться
командой ``xgettext`` из пакета утилит GNU gettext.

.. code-block:: bash

   xgettext -L Python --keyword=_:1,2 --keyword=__ -d my-super-bot

Заглянем в наш шаблон ``.pot``, и увидим, что теперь перевод имеет
строку для перевода единственного и множественного числа:

.. code-block:: pot
   :caption: locales/messages.pot
   :lineno-start: 33

   #: lesson1.py:22
   msgid "You have {} coin!"
   msgid_plural "You have {} coins!"
   msgstr[0] ""
   msgstr[1] ""

Обновим перевод каждой из локалей:

.. code-block:: bash

   pybabel update -i locales/messages.pot -d locales -D my-super-bot -l ru

и

.. code-block:: bash

   pybabel update -i locales/messages.pot -d locales -D my-super-bot -l en

При генерации Babel по коду языка сгенерировал в файле .po для каждого
языка свою формулу определения форм слова, а также сами строки для
правильного перевода каждой формы.

В английской версии у нас две формы единственное и множественное число:

.. code-block:: po
   :caption: locales/en/LC_MESSAGES/my-super-bot.po
   :lineno-start: 16

   "Plural-Forms: nplurals=2; plural=(n != 1);\n"

.. code-block:: po
   :lineno-start: 31

   #: lesson1.py:22
   msgid "You have {} coin!"
   msgid_plural "You have {} coins!"
   msgstr[0] ""
   msgstr[1] ""

Ниже Babel пометил старые строки удаленными с помощью комментария
``#~``. (У меня не было перевода в английском файле, я забыл их
добавить. Поэтому строка ``msgstr`` пустая.) Babel посчитал их не
нужными, потому что теперь появились такие же строки с множественными
формами)

.. code-block:: po
   :lineno-start: 37

   #~ msgid "You have {} coins!"
   #~ msgstr ""

В русском языке три множественных формы. Единственное, малое множественное и множественное:

.. code-block:: po
   :caption: locales/ru/LC_MESSAGES/my-super-bot.po
   :lineno-start: 16

   "Plural-Forms: nplurals=3; plural=(n%10==1 && n%100!=11 ? 0 : n%10>=2 && "
   "n%10<=4 && (n%100<10 || n%100>=20) ? 1 : 2);\n"

.. code-block:: po
   :lineno-start: 31

   #: lesson1.py:22
   #, fuzzy
   msgid "You have {} coin!"
   msgid_plural "You have {} coins!"
   msgstr[0] "У Вас {} монет!"
   msgstr[1] ""
   msgstr[2] ""

Здесь Babel сохранил наш старый перевод из предыдущего файла ``.po``, именно поэтому я говорил,
что они нам нужны в ветке development. Он пометил данный перевод как неточный ``fuzzy``, чтоб мы исправили.

Вернемся теперь к формуле. Формула для вычисления множественных форм - это обычная тернарная
условная операция на СИ-подобном языке вида ``condition ? true : false``.
И именно для ее работы мы компилируем переводы.

Итак, в английском у нас две формы слова: ``nplurals=2``. А ``plural=(n != 1);\n"``
означает формулу вычисления, по которой определяется надо ли ставить фразу в единственном числе или множественном,
в зависимости от переданного ``n``:

-  если полученное в основном коде из нашей функции ``_("You have {} coin!", "You have {} coins!", n).format(n))`` число ``n`` равно 1, то
   выражение ``n != 1`` возвращает 0 (То есть False. False неявно приводится к int и равно 0), и строки берутся из ``msgstr[0]``.
   Это единственное число.
-  если n не равно 1, то выражение ``n != 1``, то возвращает 1 (True) и
   форма слова является множественным числом. Берутся данные из ``msgstr[1]``.

Заполняем:

.. code-block:: po
   :caption: locales/en/LC_MESSAGES/my-super-bot.po

   #: lesson1.py:22
   msgid "You have {} coin!"
   msgid_plural "You have {} coins!"
   msgstr[0] "You have {} coin!"
   msgstr[1] "You have {} coins!"

Если же для языка нет перевода, то отобразятся строки ``msgid`` "You have {} coin!" и ``msgid_plural`` "You have {} coins!"

В русском языке три формы слова ``nplurals=3``. Формула
``plural=(n%10==1 && n%100!=11 ? 0 : n%10>=2 && " "n%10<=4 && (n%100<10 || n%100>=20) ? 1 : 2);\n"``
означает:

-  Если выражение ``n%10==1 && n%100!=11`` верно и ``n`` заканчивается на
   единицу, но не заканчивается на 11, то возвращается 0 (потому что в тернарном выражении
   явно указано возвращать ноль после двоеточия). Берутся данные из
   ``msgstr[0]``. И это и единственное число. То есть 1 монета, 101
   монета, но не 111 монет.
-  Иначе: вычисляем ``n%10>=2 && n%10<=4 && (n%100<10 || n%100>=20)``,
   это форма для чисел, заканчивающихся на 2, 3 и 4. Например, 3 монеты
   и 44 монеты. Если выражение верно, то возвращаем 1. Берутся данные из
   ``msgstr[1]``.
-  Иначе: возвращаем 2. И это остальные числа. 5, 11, 56, 110, 111 и т.д.
   монет. Берутся данные из ``msgstr[2]``.

Выбор перевода это просто взятие k-го элемента ``msgstr[k]``, где k
вычислено по этой формуле.

Из предыдущего перевода (старого файла .po, который мы специально не удаляли) у нас подставилась часть ранее переведенных строк.
Поэтому переводим недостающие элементы, не забываем удалить строки, помеченные для удаления, и метки неточного перевода fuzzy.

.. code-block:: po
   :caption: locales/ru/LC_MESSAGES/my-super-bot.po

   #: lesson1.py:22
   msgid "You have {} coin!"
   msgid_plural "You have {} coins!"
   msgstr[0] "У Вас {} монета!"
   msgstr[1] "У Вас {} монеты!"
   msgstr[2] "У Вас {} монет!"

Компиляция переводов, файлы формата mo.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Особенность работы с gettext и Babel заключается в том, что все файлы переводов должны быть предварительно
скомпилированы, поскольку перевод строк выбирается по индексам, рассчитанным по формулам.

Компилируем переводы командой:

.. code-block:: bash

   pybabel compile -d locales -D my-super-bot

``-d`` - имя директории locales

``-D`` - домен "my-super-bot"

И получаем в нашей локали файлы ``.mo``, радом с файлами ``.po``.

Файлы ``.mo`` храним в репозитории в ветке production, и распространяем с программой.
В отличие от файлов ``.po``, которые предназначены для разработки и хранятся в ветке development.

Финальный результат.
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python
   :caption: lesson1.py
   :linenos:

   from aiogram import Bot, Dispatcher, F, html
   from aiogram.types import Message

   from aiogram.utils.i18n import gettext as _
   from aiogram.utils.i18n import lazy_gettext as __
   from aiogram.utils.i18n import I18n, ConstI18nMiddleware

   TOKEN = "token"
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

Запускаем код, указываем константный русский язык в строке:

.. code-block:: python
   :lineno-start: 30

   dp.message.outer_middleware(ConstI18nMiddleware(locale='ru', i18n=i18n))

Тестируем. Меняем значение на ``locale='en'`` и снова запускаем и
тестируем.

.. code-block:: python
   :lineno-start: 30

   dp.message.outer_middleware(ConstI18nMiddleware(locale='en', i18n=i18n))

Для динамического переключения языков, нам нужно хранить язык в базе
данных и реализовать свой класс middleware на базе ``I18nMiddleware`` из
``aiogram.utils.i18n.middleware``. Это мы сделаем чуть позже. А пока
разберемся с еще одним инструментом для локализации и
интернационализации на базе проекта Fluent от Mozilla.
