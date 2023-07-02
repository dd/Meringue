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
	<a href="https://py-meringue.readthedocs.io/en/latest/?badge=latest">
		<img src="https://readthedocs.org/projects/py-meringue/badge/?version=latest" alt="Documentation Status" />
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
	<a href="https://github.com/pypa/hatch" target="_blank">
		<img src="https://img.shields.io/badge/%F0%9F%A5%9A-Hatch-4051b5.svg" alt="Hatch project" />
	</a>
	<a href="https://squidfunk.github.io/mkdocs-material/" target="_blank">
		<img src="https://img.shields.io/badge/docs-mkdocs%20material-blue.svg" alt="Material for MkDocs" />
	</a>
	<a href="https://github.com/charliermarsh/ruff" target="_blank">
		<img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v0.json" alt="linting - Ruff" />
	</a>
	<a href="https://github.com/psf/black" target="_blank">
		<img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="code style - black" />
	</a>
	<!-- <a href="https://github.com/python/mypy" target="_blank">
		<img src="https://img.shields.io/badge/types-Mypy-blue.svg" alt="types - Mypy" />
	</a> -->
	<a href="https://raw.githubusercontent.com/dd/Meringue/master/LICENSE" target="_blank">
		<img src="https://img.shields.io/pypi/l/meringue?color=008033" alt="License - GNU Lesser General Public License v3.0" />
	</a>
</p>

Package with various functional (such as mixins, form utils, upload handlers and other) for Django Framework.

This library is a set of various functionality that I use from project to project.

The main task of this package is to clean up this functionality, test it, and also organize the documentation so that colleagues can understand how and what works.

However, if someone decides to use this functionality in their project, and even more so to add functionality or change the implementation to a more correct, beautiful or understandable one, I will only be happy, do not worry and feel free to write to me by [mail](mailto:dd@manin.space), create an [issue](https://github.com/dd/Meringue/issues) or [pull request](https://github.com/dd/Meringue/pulls) on [github](https://github.com/dd/Meringue).


## Roadmap

### First stage

Refactoring old functionality and getting rid of unnecessary

* models
	* [x] Mixin with ctime and mtime fields
	* [x] Abstract model with sort field
		* [x] Add abstract model
		* [x] Add a manager with a method to correct sorting
		* [x] Testing
	* [x] Abstract model with publishing flag
	* [x] Abstract model with the functionality of publishing in a certain period
* i18n
	* [x] Field translation simplification functionality when using [django-modeltranslation](https://django-modeltranslation.readthedocs.io/en/latest/)
	* [x] Localization of all texts in the library
* utils
	* [x] Method and template tag for getting date range
* template tags
	* [x] Template tag for generating the year for the copyright string (like Copyright © 2014-2023)
* other
	* [x] Upload handlers with renaming uploaded files


### Second stage

Adding new functionality. Can change.

* Universal manager worked with all abstract models
* Tests of all functionality
* Methods for encrypting and decrypting text content (To create various secrets, such as a link to change your password or activate your profile).
* Functionality for obtaining absolute links to resources presented on the front, located on another domain (When working through api) (utils methods, template tags and filters).
* [drf](https://www.django-rest-framework.org/) serializer serializer for automatic form generation on the front when working through rest api. (An npm package on [vuejs](https://vuejs.org/) will also be developed
 generating form based on response from api).
* Extended [drf router](https://www.django-rest-framework.org/api-guide/routers/) that allows you to add resources like `/profile` returning the profile data of an authorized user without his id.
* Authorization backend for authorization by a pair of email and password.
* Helpers to extend documentation generated by [drf-spectacular](https://drf-spectacular.readthedocs.io/) - just a small helper to easily add links to different deployed environments (production, test, local, etc.) or let's say for more digestible tags instead of initially generated ones
* Functionality for working with images.
	* Image editor like easy_thumbnails.
	* A field for the drf serializer that returns a set of images (for example, a standard image and a double-sized image for a retina screen), as well as in different formats (for example, in the original format and in webp).
* Functionality similar to that described in the previous paragraph only for video.
* Functionality for loading private files available through [nginx internal](http://nginx.org/en/docs/http/ngx_http_core_module.html#internal).
* Exception handler for drf that returns an error code in addition to the error text




## Contributing

- [x] Use Git Flow (read [here](https://jeffkreeftmeijer.com/git-flow/) and [here](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow)) to resolve the versioning
- [x] Linter with a [Ruff](https://github.com/charliermarsh/ruff)
- [x] Formatter with a [Black](https://github.com/psf/black)
- [x] Lint commit with [Gitlint](https://jorisroovers.com/gitlint/) and [Conventional Commits](https://www.conventionalcommits.org/)
- [x] Documentation with [mkdocs](https://www.mkdocs.org/) and [mkdocs-material](https://squidfunk.github.io/mkdocs-material/)
- [x] Testing local with [hatch](https://hatch.pypa.io/1.7/meta/faq/#environments)
- [ ] Testing in CI/CD on push
- [ ] Add [mypy](https://mypy-lang.org/) ???
