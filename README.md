# Meringue

Package with various functional (such as mixins, form utils, upload handlers and other) for Django Framework.


## Roadmap

* Refactoring all functional

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



## Contributing

- [x] Use Git Flow (read [here][git_flow] and [here][git_flow_atlassian]) to resolve the versioning
- [ ] Documentation with [mkdocs](https://www.mkdocs.org/) or [antora](https://antora.org/)
- [ ] Testing with [hatch](https://hatch.pypa.io/1.7/meta/faq/#environments) or [tox](https://tox.wiki/en/latest/)
- [ ] Linter and formatter with a [Ruff](https://beta.ruff.rs/docs/) and [Black](https://github.com/psf/black)
- [ ] Lint commit with [Gitlint](https://jorisroovers.com/gitlint/) and [Conventional Commits](https://www.conventionalcommits.org/)
- [ ] Add [mypy](https://mypy-lang.org/) ???


[git_flow]: https://jeffkreeftmeijer.com/git-flow/
[git_flow_atlassian]: https://www.atlassian.com/ru/git/tutorials/comparing-workflows/gitflow-workflow
