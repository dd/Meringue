# Contributing

Please don't be shy - comment, discuss and suggest whatever you think is important in the [discussions](https://github.com/dd/Meringue/discussions) on github, if you notice a bug please describe it in [issues](https://github.com/dd/Meringue/issues), and if you decide to contribute to the development of the project, feel free to send [pull request](https://github.com/dd/Meringue/pulls), and if possible, read further during development this section.

When developing, modifying and fixing a feature, please fill in and correct all annotations and docstrings in the code, and also try, if possible, to fill in / supplement the description of the functionality and its use in the [section](../../usage) of the documentation, also add tests for new or fixed functionality, read more below:


## Environment

To work, you need a configured environment, for this there is the following script:

```console
$ hatch run init
```

!!! note
	All development is done using [hatch](https://hatch.pypa.io/). To work with it, you will need to install it globally, I advise you to do this using [pipx](https://github.com/pypa/pipx).

This script will completely configure the environment - configure gitflow, connect git hooks, and install and configure a virtual environment, to run python in this environment, run the following command:

```console
$ hatch run ipython
```


## Git flow

As you develop and refine, please try to keep your repository consistent with [gitflow](https://github.com/petervanderdoes/gitflow-avh).


## Internationalization

Что бы добавить переводы есть две полезные комманды:

### `makemessages`

```console
$ hatch run makemessages
```

Это команда обёртка над джанговской командой [makemessages](https://docs.djangoproject.com/en/4.2/ref/django-admin/#makemessages) и создаёт / обновляет файлы локализации в каждом приложении _meringue_.


### `compilemessages`

```console
$ hatch run compilemessages
```

Это команда обёртка над джанговской командой [compilemessages](https://docs.djangoproject.com/en/4.2/ref/django-admin/#compilemessages) и компилирует все переводы.


## Tests

When working on a project, it is extremely important to cover everything with tests in order to avoid problems and errors in the code. See working on tests in the appropriate [section](../tests).


## Documentation

The documentation is implemented using the [mkdocs](https://www.mkdocs.org/) generator and the [mkdocs material](https://squidfunk.github.io/mkdocs-material/) theme. When working on library functionality, two main sections [usage](../../usage) and [reference](../../reference/meringue/conf/__init__/) are important. For more information about developing documentation, see the corresponding [section](../docs).


## Versioning

::: meringue.__version__
	options:
		show_root_heading: false
		show_root_toc_entry: false


## Commit message convention

To write a commit, we adhere to the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) specification, as well as [gitmoji](https://gitmoji.dev/) as a special case of _conventional commits_. You can use [gitmoji-cli](https://github.com/carloscuesta/gitmoji-cli) for this process. This will help us generate a changelog (and in the future we may automate this based on commits).

!!! info
	The list of emoji needs to be improved, now it is bloated and there are controversial points like :fire: which means deleting the code...
