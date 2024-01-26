# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
# Это был пример лицензии

### Файл примера перевода на английский язык
### Логика перевода изменится, не затрагивая код и другие переводы
### С тройного шарпа начинается комментарий уровня файла

## Это комментарий уровня группировки блоков в тексте. См. документацию.
## Hello section

# Это пример термина. Термин начинается с дефиса.
# Посмотрите как это работало в русском переводе. Здесь же мы изменим логику.
# Падежи нам не нужны, но может потребоваться притяжательная форма
-telegram = { $case ->
     *[common] Telegram
      [possessive] Telegram's
    }

# { $user } - user name, { $language } - language code.
# Это было описание переменных, которые попадают сюда из основного кода приложения.
# Термин мы берем из этого же файла перевода,
# и вставляем с параметром нужного контекста использования (в нашем случае падежа).
hello = Hi, <b>{ $user }</b>!
    { $language ->
     [None] In your { -telegram(case: "common") } client a language isn't set.
            Therefore, everything will be displayed in default language.
    *[any] Your Telegram client is set to { $language }. Therefore, everything will be displayed in this language.
    }

help = { $case ->
    *[capital] Help
     [lower] help
    }
help-message =
    <b>Welcome to the bot.</b>
    Our bot can't do anything useful, but it can switch languages with dexterity.

    The following commands are available in the bot:
    /start to start working with the bot.
    /help or just send the word <b><i>help</i></b> to show this message.
    /language_en { switch-to-en }
    /language_ru { switch-to-ru }
    /photo or just send the word <b><i>photo</i></b> to send photo to you.


# { $language } - language code.
# The current language is { $language }.
cur-lang = The current language is: <i>{ $language }</i>

## Switch language section

# Название языка мы отображаем на родном языке, чтоб человек увидел знакомые буквы и поонял, что не все потеряно.
en-lang = English
ru-lang = Русский
switch-to-en = Switch the interface to { en-lang }.
switch-to-ru = Switch the interface to { ru-lang }.
lang-is-switched = Display language is { en-lang }.

photo = photo

## Common messages section

i-dont-know = I'm so stupid bot. Make me clever.
show-date = But look! Pretty date on English: { DATETIME($date_, month: "long", year: "numeric", day: "numeric", weekday: "long") }
