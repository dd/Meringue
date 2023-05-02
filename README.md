<h1 align="center" >Meringue</h1>

<!-- | CI/CD | [![CI - Test](https://github.com/pypa/hatch/actions/workflows/test.yml/badge.svg)](https://github.com/pypa/hatch/actions/workflows/test.yml) [![CD - Build Hatch](https://github.com/pypa/hatch/actions/workflows/build-hatch.yml/badge.svg)](https://github.com/pypa/hatch/actions/workflows/build-hatch.yml) [![CD - Build Hatchling](https://github.com/pypa/hatch/actions/workflows/build-hatchling.yml/badge.svg)](https://github.com/pypa/hatch/actions/workflows/build-hatchling.yml) |
| Docs | [![Docs - Release](https://github.com/pypa/hatch/actions/workflows/docs-release.yml/badge.svg)](https://github.com/pypa/hatch/actions/workflows/docs-release.yml) [![Docs - Dev](https://github.com/pypa/hatch/actions/workflows/docs-dev.yml/badge.svg)](https://github.com/pypa/hatch/actions/workflows/docs-dev.yml) | -->
<p align="center">
	<a href="https://pypi.org/project/meringue">
		<img src="https://img.shields.io/pypi/status/meringue.svg" alt="PyPI - Status" />
	</a>
	<a href="https://pypi.org/project/meringue">
		<img src="https://img.shields.io/pypi/v/meringue.svg" alt="PyPI - Version" />
	</a>
	<a href="https://pypi.org/project/meringue">
		<img src="https://img.shields.io/pypi/dm/meringue.svg" alt="PyPI - Downloads" />
	</a>
	<!-- <a href="https://pypi.org/project/meringue">
		<img src="https://img.shields.io/pypi/frameworkversions/django/meringue.svg" alt="PyPI - Django Framework Version" />
	</a> -->
	<!-- <a href="https://pypi.org/project/meringue">
		<img src="https://img.shields.io/pypi/pyversions/meringue.svg" alt="PyPI - Python Version" />
	</a> -->
	<!-- <a href="https://pypi.org/project/meringue">
		<img src="https://img.shields.io/pypi/format/meringue.svg" alt="PyPI - Format" />
	</a> -->
</p>
<p align="center">
	<a href="https://github.com/pypa/hatch">
		<img src="https://img.shields.io/badge/%F0%9F%A5%9A-Hatch-4051b5.svg" alt="Hatch project" />
	</a>
	<a href="https://github.com/charliermarsh/ruff">
		<img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v0.json" alt="linting - Ruff" />
	</a>
	<a href="https://github.com/psf/black">
		<img src="https://img.shields.io/badge/code%20style-Black-000000.svg" alt="code style - Black" />
	</a>
	<!-- <a href="https://github.com/python/mypy">
		<img src="https://img.shields.io/badge/types-Mypy-blue.svg" alt="types - Mypy" />
	</a> -->
	<a href="https://raw.githubusercontent.com/dd/Meringue/master/LICENSE">
		<img src="https://img.shields.io/pypi/l/meringue?color=008033" alt="License - GNU Lesser General Public License v3.0" />
	</a>
</p>


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

- [x] Use Git Flow (read [here](https://jeffkreeftmeijer.com/git-flow/) and [here](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow)) to resolve the versioning
- [x] Linter with a [Ruff](https://github.com/charliermarsh/ruff)
- [x] Formatter with a [Black](https://github.com/psf/black)
- [ ] Lint commit with [Gitlint](https://jorisroovers.com/gitlint/) and [Conventional Commits](https://www.conventionalcommits.org/)
- [ ] Documentation with [mkdocs](https://www.mkdocs.org/) or [antora](https://antora.org/)
- [ ] Testing with [hatch](https://hatch.pypa.io/1.7/meta/faq/#environments) or [tox](https://tox.wiki/en/latest/)
- [ ] Add [mypy](https://mypy-lang.org/) ???
