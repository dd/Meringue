# Contributing

Please feel free to suggest and comment on anything that doesn't seem right.


## Environment

First, you need a globally installed [hatch](https://hatch.pypa.io/) (suggest doing this using [pipx](https://github.com/pypa/pipx)).

Before starting work, you must run the initialization script:

```bash
hatch run init
```

This script will completely set up the environment, as well as configure gitflow and connect git hooks.


## Documentation

The server for local development can be started with the following command:

```bash
hatch run docs:serve
```

!!! note
	The first time the command will run for a long time, as the environment will be configured

For more information on developing documentation, see the relevant [section][documentation].


## Development

When developing a feature, be sure to add all the annotations, docstrings, detailed descriptions of how to use it in the appropriate [section](../../usage) documentation and write tests.


### Git flow

While developing and finalizing, keep the repository in accordance with [gitflow](https://github.com/petervanderdoes/gitflow-avh).


### Commit message convention

When committing changes, take care of the correct commit header according to [conventionalcommits](https://www.conventionalcommits.org/en/v1.0.0/) and [gitlint](https://jorisroovers.com/gitlint/latest/) settings project.


### Versioning

::: meringue.__version__
    options:
      show_root_heading: false
      show_root_toc_entry: false
