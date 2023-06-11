# Documentation

Для разработки документации используется [mkdocs](https://www.mkdocs.org/) с темой [mkdocs-material](https://squidfunk.github.io/mkdocs-material/).

Исходники для генерации документации парсит [mkdocstring-python](https://mkdocstrings.github.io/python/), который может работать с [несколькими форматами](https://mkdocstrings.github.io/python/usage/configuration/docstrings/#docstring_style), у нас используется _Google-style_ (это касается только докстрингов), однако не [чистый](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings), а его вариация [napoleon](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html) (Но конечно это вопрос обсуждаемый, и можем изменить, если есть предложения).

!!! abstract
	Давайте, по возможности, в документации писать все заголовки на английском, в таком случае все якоря будут генериться на английском.


## Local development

В самом простом случае запуск локального сервера с документацией для разработки будет выглядеть следующим образом:

```bash
hatch run docs:serve
```


## Configuration

Есть несколько параметров для конфигурации документации:


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
