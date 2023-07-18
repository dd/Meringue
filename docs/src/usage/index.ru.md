# Getting Started


## Installation

```console
$ pip install meringue
```

Подключать можно отдельные модули по необходимости (подробнее читай в документации соответствующего модуля):

```pycon
INSTALLED_APPS = (
    ...
    'meringue.core',
    ...
)
```


Все настройки для библиотеки указываются внутри параметра `MERINGUE` (подробнее в соответствующем [разделе](./conf.md)):

```pycon
MERINGUE = {
    ...
}
```
