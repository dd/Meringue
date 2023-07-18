# Contributing

Пожалуйста, не стесняйся - комментируй, обсуждай и предлагай всё что тебе кажется важным в [обсуждениях](https://github.com/dd/Meringue/discussions) на github, если заметил баг опиши в [issues](https://github.com/dd/Meringue/issues), а если решишь внести свою лепту в развитие проекта смело отправляй [pull request](https://github.com/dd/Meringue/pulls), и по возмости при разработке прочитай далее этот раздел.

Разрабатывая, дорабатывая и исправляя фичу, пожалуйста, заполни и поправь все аннотации и докстринги в коде, а также постарайтесь по возможности заполнить / дополннить описание функционала и его использование в [разделе](../../usage) документации, так же добавь тесты для нового или исправленого функционала, подробнее почитай далее:


## Environment

Для работы тебе понадобится настроенное окружение, для этого есть следующий скрипт:

```console
$ hatch run init
```

!!! note
	Вся разработка ведётся с использование [hatch](https://hatch.pypa.io/). Что бы с ним работать тебе понадобится его поставить глобально я советую это делать с помощью [pipx](https://github.com/pypa/pipx).

Этот скрипт полностью настроит окружение - сконфигурирует gitflow, подключит git хуки, а так же установит и настроет виртуальное окружение, что бы запустить python в этом окружжении запусти следующую команду:

```console
$ hatch run ipython
```


## Git flow

Разрабатывая и дорабатывая, пожалуйста, постарайся вести репозиторий в соответствии с [gitflow](https://github.com/petervanderdoes/gitflow-avh).

!!! question
	Вероятно этот момент изменится, библиотека активно разрабатывается, я выбрал этот подход как знакомый, однако, думаю что нужно будет изменить его. Если есть предложенния с радостью выслушаю.


## Internationalization

Чтобы добавить переводы есть две полезные комманды:


### `makemessages`

```console
$ hatch run makemessages
```

Это команда обёртка над джанговской командой [makemessages](https://docs.djangoproject.com/en/4.2/ref/django-admin/#makemessages) и создаёт/обновляет файлы локализации в каждом приложении _meringue_.


### `compilemessages`

```console
$ hatch run compilemessages
```

Это команда обёртка над джанговской командой [compilemessages](https://docs.djangoproject.com/en/4.2/ref/django-admin/#compilemessages) и компилирует все переводы.


## Tests

При работе над проектом, крайне важно охватить всё тестами, во избежание проблем и ошибок в коде. Ознакомься с работай над тестами в соответствующем [разделе](/dev/tests).


## Documentation

Документация реализована с помощью генератора [mkdocs](https://www.mkdocs.org/) и темы [mkdocs material](https://squidfunk.github.io/mkdocs-material/). При работе над функционалом библиотеки важны два основных раздела [usage](../../usage) и [референс](../../reference/meringue/conf/__init__/). Подробнее о разработке документации смотрите в соответствующем [разеделе](/dev/docs).


## Versioning

::: meringue.__version__
	options:
		show_root_heading: false
		show_root_toc_entry: false


## Commit message convention

Для написания коммита придерживаемся спецификации [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/), а так же [gitmoji](https://gitmoji.dev/) как частного случая _conventional commits_. Для данного процесса можно использовать [gitmoji-cli](https://github.com/carloscuesta/gitmoji-cli). Это необходимо для автоматического формирования [changelog](#changelog-generation).

!!! info
	Необходимо доработать список эмоджи, сейчас он раздут и есть спорные моменты как например :fire: который означает удаление кода...


## Changelog generation

Сгенерировать Changelog можно следующей командой с использованием [gitmoji-changelog](https://github.com/frinyvonnick/gitmoji-changelog):

```console
gitmoji-changelog update 1.0.0 --preset generic --group-similar-commits
```


## Building and publishing

Для билда используется [hatch](https://hatch.pypa.io/) и что бы сбилдить библиотеку есть следующая команда:

```console
$ hatch build
```

Эту команду предоставляет hatch и подробнее о том как она работает лучше посмотреть в [документации](https://hatch.pypa.io/latest/cli/reference/#hatch-build) hatch.

Билд и выгрузка релизов реализована в [GitHub Actions](https://docs.github.com/en/actions) и происходит автоматически при пушах релизных тегов вида `v*`.

Подробнее как настрое билд и выгрузка можно ознакомиться в [конфиге](https://github.com/dd/Meringue/blob/master/.github/workflows/release.yml) workflow.
