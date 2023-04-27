# Meringue

Package with various functional (such as mixins, form utils, upload handlers and other) for Django Framework.


## Roadmap

* Using [gitflow](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow)
* Refactoring all functional
* Documentation with [mkdocs](https://www.mkdocs.org/) or [antora](https://antora.org/)
* Linter and formatter with a [Ruff](https://beta.ruff.rs/docs/) and [Black](https://github.com/psf/black)
* Add [mypy](https://mypy-lang.org/) ???
* Testing with [hatch](https://hatch.pypa.io/1.7/meta/faq/#environments) or [tox](https://tox.wiki/en/latest/)


* css для PreviewImageField
* thumbnail:

  - watermark
  - определение лица и использование в роли центра изображения
  - указание максимальной ширины или высоты
  - определение фокуса

* PreviewImageFileInput:

  - информация о изображении
  - изображение при инициализации
  - при загрузке изображения сразу же его выводить в превью (js)

* Абстрактная модель для создания галлереи со всеми необходимыми полями, кроме родительской таблицы
* тестирование
* настройки вроде DEBUG из админки
* перезагрузка сервера из админки
* put_js преобразовывать относительные пути
* тег add_attrs добавляющий всё чтопередано атрибутами тега
