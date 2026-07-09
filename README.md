<h1 align="center" >Meringue</h1>

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
	<a href="https://pypi.org/project/meringue">
		<img src="https://img.shields.io/pypi/pyversions/meringue.svg" alt="PyPI - Python Version" />
	</a>
	<a href="https://pypi.org/project/meringue">
		<img src="https://img.shields.io/pypi/frameworkversions/django/meringue" alt="PyPI - Versions from Framework Classifiers" />
	</a>
	<!-- <a href="https://pypi.org/project/meringue">
		<img src="https://img.shields.io/pypi/format/meringue.svg" alt="PyPI - Format" />
	</a> -->
</p>
<p align="center">
	<a href="https://github.com/dd/Meringue/actions/workflows/mkdocs-release.yml" >
		<img src="https://img.shields.io/github/actions/workflow/status/dd/Meringue/mkdocs-release.yml?logo=github&label=docs" alt="Documentation - Release" />
	</a>
	<a href="https://github.com/dd/Meringue/actions/workflows/test.yml" >
		<img src="https://img.shields.io/github/actions/workflow/status/dd/Meringue/test.yml?logo=github&label=tests" alt="Tests - Running" />
	</a>
	<a href="https://codecov.io/gh/dd/Meringue" >
		<img src="https://codecov.io/gh/dd/Meringue/branch/master/graph/badge.svg?token=HV1QGD74EK" alt="Tests - Coverage" />
	</a>
</p>
<p align="center">
	<a href="https://github.com/pypa/hatch" target="_blank">
		<img src="https://img.shields.io/badge/%F0%9F%A5%9A-Hatch-4051b5.svg" alt="Hatch project" />
	</a>
	<a href="https://gitmoji.dev" target="_blank">
		<img src="https://img.shields.io/badge/gitmoji-%20😜%20😍-FFDD67.svg" alt="Gitmoji" />
	</a>
	<a href="https://squidfunk.github.io/mkdocs-material/" target="_blank">
		<img src="https://img.shields.io/badge/-Material_for_MkDocs-526CFE?logo=MaterialForMkDocs&logoColor=white&labelColor=gray" alt="Built with Material for MkDocs" />
	</a>
	<a href="https://github.com/charliermarsh/ruff" target="_blank">
		<img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json" alt="linting - Ruff" />
	</a>
	<a href="https://github.com/psf/black" target="_blank">
		<img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="code style - black" />
	</a>
	<!-- <a href="https://github.com/python/mypy" target="_blank">
		<img src="https://img.shields.io/badge/types-Mypy-blue.svg" alt="types - Mypy" />
	</a> -->
	<a href="https://raw.githubusercontent.com/dd/Meringue/master/LICENSE" target="_blank">
		<img src="https://img.shields.io/pypi/l/meringue?cache-cracker" alt="License - Mozilla Public License Version 2.0" />
	</a>
</p>


A package providing various utilities for Django, such as mixins, form tools, upload handlers, and more.

This library is a collection of reusable components that I frequently use across different projects. Its primary purpose is to clean up and standardize these tools, ensure they are well-tested, and provide clear documentation to make it easy for colleagues to understand and use.

If you decide to use this in your project, or want to improve the implementation, feel free to reach out by [mail](mailto:dd@tovarisch.engineer), create an [issue](https://github.com/dd/Meringue/issues) or [pull request](https://github.com/dd/Meringue/pulls) on [GitHub](https://github.com/dd/Meringue). Contributions are always welcome!

Read more in the [documentation](https://dd.github.io/Meringue/).


## Roadmap

Adding new functionality. Can change.

* [ ] [DRF](https://www.django-rest-framework.org/) serializer for automatic form generation on the frontend via REST API. (An npm package for [Vue.js](https://vuejs.org/) will also be developed to generate forms based on API responses).
* [ ] Authentication backend for email and password login.
* [ ] Functionality for working with images.
	* [x] Image editor like easy_thumbnails.
	* [x] A DRF serializer field that returns a set of images in multiple sizes (e.g., standard and 2x for retina) and formats (e.g., original and WebP).
	* [ ] Job chain presets
	* [x] Tests
	* [x] Docs
* [ ] Similar image-processing functionality but for video.
* [x] Functionality for loading private files available through [nginx internal](http://nginx.org/en/docs/http/ngx_http_core_module.html#internal).


## Contributing

- [x] Use Git Flow (read [here](https://jeffkreeftmeijer.com/git-flow/) and [here](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow)) to resolve the versioning
- [x] Linting with [Ruff](https://github.com/charliermarsh/ruff)
- [x] Formatting with [Black](https://github.com/psf/black)
- [x] Lint commit with [Gitlint](https://jorisroovers.com/gitlint/) and [Conventional Commits](https://www.conventionalcommits.org/)
- [x] Documentation with [mkdocs](https://www.mkdocs.org/) and [mkdocs-material](https://squidfunk.github.io/mkdocs-material/)
- [x] Testing local with [hatch](https://hatch.pypa.io/1.7/meta/faq/#environments)
- [x] Testing in CI/CD on push
- [ ] Add [mypy](https://mypy-lang.org/) ???
