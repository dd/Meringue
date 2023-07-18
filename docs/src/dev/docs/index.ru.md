# Documentation

Для разработки документации используется [mkdocs](https://www.mkdocs.org/) с темой [mkdocs-material](https://squidfunk.github.io/mkdocs-material/).

Исходники для генерации документации парсит [mkdocstring-python](https://mkdocstrings.github.io/python/), который может работать с [несколькими форматами](https://mkdocstrings.github.io/python/usage/configuration/docstrings/#docstring_style), у нас используется _Google-style_ (это касается только докстрингов), однако не [чистый](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings), а его вариация [napoleon](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html) (Но конечно это вопрос обсуждаемый, и можем изменить, если есть предложения).

!!! abstract
	Давайте, по возможности, в документации писать все заголовки на английском, в таком случае все якоря будут генериться на английском.


## Local development

В самом простом случае запуск локального сервера с документацией для разработки будет выглядеть следующим образом:

```console
$ hatch run docs:serve
```


## Configuration

Есть несколько параметров для конфигурации документации:


### `MERINGUE_MKDOCS_CODE_PARCE_ENABLED`

`default: true`

Включение / отключение вывода исходников в документации "на лету" (организовано на основе примера из документации [mkdocstrings](https://mkdocstrings.github.io/recipes/#automatic-code-reference-pages)).


### `MERINGUE_MKDOCS_CODE_PARCE_SOURCE_PATH`

`default: "meringue"`

Каталог с исходниками, для генерации "на лету".


### `MERINGUE_MKDOCS_CODE_PARCE_DOCS_PATH`

`default: "reference"`

Директория в документации для вывода сгенерированной "на лету" документации по исходникам.


### `MERINGUE_MKDOCS_CODE_PARCE_SHOW_NAV`

`default: false`

Параметр для отладки генерируемой "на лету" навигации.


### `MERINGUE_MKDOCS_ENABLED_GIT_REVISION_DATE`

`default: true`

Параметр для включения / отключения дат изменения файлов документации. Будет полезно для отключения при локальной разработки, что бы консоль не забивалась ошибками.


### `MERINGUE_MKDOCS_OFFLINE`

`default: false`

Параметр для сборки документации в билд работающий из папки, без необходимости запускать сервер. подробнее о механизме читать [тут](https://squidfunk.github.io/mkdocs-material/setup/building-for-offline-usage/).


### `MERINGUE_MKDOCS_ENABLE_MINIFY`

`default: true`

Параметр для включения плагина [minify](https://github.com/byrnereese/mkdocs-minify-plugin) минифицирующий html, js и css при генерации документации.

При работе с [локальным сервером][local-development] документации параметр отключён.


## Building and publishing

Для сборки документации есть отдельная команда `hatch run docs:build`.

Но перед тем как запушить обновлённую документацию запусти пожалуйста команнду `hatch run docs:build-check`, она сбилдит документацию и проверит ссылки, на наличие битых.

Документация собирается в [GitHub Actions](https://docs.github.com/en/actions) и выгружается в ветку [gh-pages](https://github.com/dd/Meringue/tree/gh-pages) и публикуется с использованием [GitHub Pages](https://pages.github.com/).

Документация автоматически собирается и выкатывается при пуше релизного тега (`v*`), а так же при пуше в `dev` ветку обновляется дев версия документации. Подробнее о этих процессах ты можешь изучить в конфигах для [релиза](https://github.com/dd/Meringue/blob/master/.github/workflows/mkdocs-release.yml) и [дев](https://github.com/dd/Meringue/blob/master/.github/workflows/mkdocs-dev.yml) workflow.
