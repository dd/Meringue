# Tests

В проекте используется [pytest](https://docs.pytest.org/) для тестирования, а так же настроены тесты покрытия с использование [pytest-cov](https://pytest-cov.readthedocs.io/), крайне рекомендуется к ознакомлению.


## Usage

Запустить тесты в окружении для разработки можно следующей командой:

```console
$ hatch run test:check
```

Так же в hatch настроена матрица для набора версий python и django, подробнее об этом можно посмотреть в настройках в файле `pyproject.toml`, запустить всю матрицу тестов можно скриптом hatch:

```console
$ hatch run mtest:check
```


## Development

При разработке тестов может понадобиться создать новые миграции, это можно сделать следующей командой:

```console
$ hatch run test:django-admin makemigrations
```

Приложение используемое в тестах лежит в каталоге `test_project`.

База данных используется SQLite в памяти.


## Autotests

Автоматически тесты отпрабатывают при пуше в `master` и релизные ветки `release/*`. За подробностями изучи [конфиг](https://github.com/dd/Meringue/blob/master/.github/workflows/test.yml) workflow.

В процессе результаты тестов выгружаются на [codecov.io](https://app.codecov.io/gh/dd/Meringue).
