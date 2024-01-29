# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
# Это был пример лицензии

### Файл примера перевода на русский язык
### Важно. Не забудь полить помидоры...
### С тройного шарпа начинается комментарий уровня файла

## Это комментарий уровня группировки блоков в тексте. См. документацию.
## Hello section

# Это пример термина. Термин начинается с дефиса.
# Термины можно передавать внутри сообщений, указывая переменные для параметризации в скобках.
# То есть это как атрибуты, но мы их задаем в тексте переводов, а не получаем извне.
# Мы будем издеваться над языком, чтобы увидеть как и что работает
-telegram = {$case ->
    *[nominative] Телеграм {"{"}Telegram{"}"}
     [genitive] Телеграма ({"{"}Telegram'а{"}"})
     [dative] Телеграму ({"{"}Telegram'у{"}"})
     [accusative] Телеграм ({"{"}Telegram{"}"})
     [instrumental] Телеграмом ({"{"}Telegram'ом{"}"})
     [prepositional] Телеграме ({"{"}Telegram'е{"}"})
    }
# {"}"}  это пример экранированного символа.
# Падежи
# nominative - именительный
# genitive - родительный
# dative - дательный
# accusative - винительный
# instrumental творительный.
# prepositional - предложный

# { $user } - user name, { $language } - language code.
# Это было описание переменных, которые попадают сюда из основного кода приложения.
# Термин мы берем из этого же файла перевода,
# и вставляем с параметром нужного контекста использования (в нашем случае падежа).
hello = Привет, <b>{ $user }</b>!
        У тебя в клиенте { -telegram(case: "nominative") } { $language ->
     [None] не указан язык, поэтому все будет отображается на языке по-умолчанию.
    *[any] указан язык { $language }, поэтому все будет отображается на этом языке.
    }

# а так мы вставляем символы unicode по номеру \uHHHH. Например,
# tears-of-joy1 = {"\U01F602"}
# tears-of-joy2 = 😂

help = { $case ->
    *[capital] Помощь
     [lower] помощь
    }

help-message =
    <b>Добро пожаловать в бота.</b>
    Наш бот не умеет ничего полезного, однако с ловкостью может переключать язык.

    В боте доступны следующие команды:
    /start чтобы начать работать с ботом
    /help или просто отправьте слово <b><i>помощь</i></b>, чтобы показать это сообщение
    /language_en { switch-to-en }
    /language_ru { switch-to-ru }
    /photo или просто отправьте слово <b><i>фото</i></b>, чтобы прислать вам картинку


# Это комментарий подсказка для переводчиков (чтобы не искать что значат эти переменные в коде,
# который не факт ,что они получат, а если и получат, то не поймут:

# { $language } - language code.
# The current language is { $language }.
cur-lang = Текущий язык: <i>{ $language }</i>

## Switch language section

en-lang = English
ru-lang = Русский
switch-to-en = Переключить интерфейс на { en-lang } язык.

# В фигурных скобках пример интерполяции одного сообщения в другом.
switch-to-ru = Переключить интерфейс на { ru-lang } язык.
lang-is-switched = Язык переключен на { ru-lang }.

photo = фото

## Common messages section

i-dont-know = Я тупой бот. Сделай меня умным.
show-date = Но посмотри! Красивая дата по правилам Русского языка: { DATETIME($date_, month: "long", year: "numeric", day: "numeric", weekday: "long") }