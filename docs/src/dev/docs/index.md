# Documentation

Для разработки документации мы используем [mkdocs](https://www.mkdocs.org/) с темой [material](https://squidfunk.github.io/mkdocs-material/).


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


## Building and publishing
