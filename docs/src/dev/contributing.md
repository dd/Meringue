# Contributing



## Environment

Во первых необходим глобально установленный [hatch](https://hatch.pypa.io/) (я предлагаю делать это с использованием [pipx](https://github.com/pypa/pipx)).

Перед стартом работы необходимо запустить скрипт инициализации:

```bash
hatch run init
```

Этот скрипт полностью настроит окружение, а так же сконфигурирует gitflow и подключит git хуки.


## Documentation

Сервер для локальной разработки можно запустить следующей командой:

```bash
hatch run docs:serve
```

!!! note
	Первый раз команда будет запускаться долго, так как будет настраиваться окружение


## Development

Разрабатывая фичу озаботься описанием её в документации


### Git flow

Разрабатывая и дорабатывая, веди репозиторий в соответствии с [gitflow](https://github.com/petervanderdoes/gitflow-avh)


### Commit message convention

Фиксируя изменения, озаботься правильным заголовком коммита


### Versioning

::: meringue.__version__
    options:
      show_root_heading: false
      show_root_toc_entry: false
