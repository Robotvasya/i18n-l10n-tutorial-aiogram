Глава 4. Локализация и интернационализация на базе проект Fluent от Mozilla.
----------------------------------------------------------------------------

Знакомство с Fluent
~~~~~~~~~~~~~~~~~~~~~~~~~~

**Fluent** — это семейство спецификаций, реализаций и практик
локализации, разработанных компанией Mozilla, при разработке своего
браузера Firefox и сопутствующих продуктов. С проектом Fluent вы можете
ознакомиться здесь: `<https://projectfluent.org/>`_ и реализацией под Python:
`<https://github.com/projectfluent/python-fluent>`_

Отвлечемся от кода и поговорим о процессе разработки. Одной из
постоянных задач глобальной разработки программного обеспечения является
сокращение технического долга и устаревшего кода. Расстановка
приоритетов имеет место, когда становится ясно, что организации
необходимо заменить устаревший код чем-то более эффективным и
современным. Очень часто устаревший код, влияющий на интернационализацию
(i18n) и локализацию (l10n), оказывается одной из последних областей
кодовой базы, которым уделяется приоритетное внимание.

Согласно традиционному процессу локализации программного обеспечения,
локализованный продукт создается в результате объединения статических
языковых ресурсов в исполняемый файл, который затем распространяется
среди пользователей. Любое обновление этих языковых ресурсов требует
создания нового исполняемого файла и передачи его пользователям по
цепочке распространения. По этой причине большинство
компаний-разработчиков программного обеспечения предпочитают откладывать
обновления локализации с момента их доступности до момента, когда их
можно будет объединить с другими улучшениями программного обеспечения.

С помощью Fluent этот процесс можно разделить, что позволяет выпускать
обновления локализации независимо от более широкого графика выпуска.
Языковые ресурсы не являются частью программного пакета, а доставляются
пользователям посредством безопасных вызовов API при запуске
программного обеспечения. Более того, эти вызовы API позволяют
доставлять обновления локализации без вмешательства пользователя — нет
необходимости вручную инициировать обновление, а в некоторых случаях
даже перезапускать программное обеспечение.

Еще одна проблема, которую решает проект, в локализации программного
обеспечения доминирует устаревшая парадигма: перевод представляет собой
всего лишь словарь строк, которые взаимно однозначно сопоставляются с
английской (en-US) копией. Эта парадигма несправедлива и ограничивает
языки с более сложной грамматикой, чем английская. Для любой
грамматической функции, не поддерживаемой английским языком, в исходный
код должен быть добавлен специальный случай, что приводит к пробросу
этой логики во все переводы. Более того, создание хороших
пользовательских интерфейсов, которые зависят от множества внешних
аргументов, сложно и требует от разработчика понимания грамматики
языков, на которые нацелен продукт.

Fluent поддерживает ассиметричную локализацию. Асимметричная локализация
не ограничивается множественным числом. Свободный перевод может
варьироваться в зависимости от пола, грамматического падежа,
операционной системы и многих других переменных. Все это происходит
изолированно. То, что один язык имеет преимущества более
продвинутой логики, не требует какой-либо другой локализации для его
применения. Каждая локализация контролирует сложность перевода. То есть
Fluent дает переводчикам возможность создавать грамматически правильные
переводы и использовать выразительную силу своего языка, не влияя на другие переводы.

Кроме этого, более гибок процесс отображения непереведенных элементов.
Он не привязан жестко к английскому варианту, а выбирается из цепочки
резервных локалей, которые понимает конкретный не англоговорящий пользователь.

Обзорную статью можно посмотреть здесь:
`<https://multilingual.com/issues/sept-oct-2019/fluent-firefoxs-new-localization-system/>`_

Хорошие практики и описание почему при переводе надо отказаться от
принципа DRY (Don’t Repeat Yourself) в пользу принципа WET (Write
Everything Twice), вы можете прочитать здесь:
`<https://github.com/projectfluent/fluent/wiki/Good-Practices-for-Developers>`_

Вообще интернационализация и локализация заставляют применять очень разнообразные подходы
к разработке программного обеспечения. Приходится совмещать несовместимые вещи,
такие как избежание дублирования кода с многократным повторением кода и текстов,
адаптированных под национальные особенности.
