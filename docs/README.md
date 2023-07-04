# Documentation

To develop documentation, use [mkdocs](https://www.mkdocs.org/) with the theme [mkdocs-material](https://squidfunk.github.io/mkdocs-material/).

Sources for documentation generation parse [mkdocstring-python](https://mkdocstrings.github.io/python/) which can handle [multiple formats](https://mkdocstrings.github.io/python/usage/configuration/docstrings/#docstring_style), we use _Google-style_ (this only applies to docstrings), but not [pure](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings), and its variation is [napoleon](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html) (But of course this is a debatable issue, and we can change if there are suggestions).


## Local development

In the simplest case, running a local server with development documentation would look like this:

```console
$ hatch run docs:serve
```


## Configuration

There are several options for documentation configuration:


### `MERINGUE_MKDOCS_CODE_PARCE_ENABLED`

`default: true`

Enabling / disabling the output of sources in the documentation "on-the-fly" (organized based on the example from the [mkdocstrings](https://mkdocstrings.github.io/recipes/#automatic-code-reference-pages) documentation).


### `MERINGUE_MKDOCS_CODE_PARCE_SOURCE_PATH`

`default: "meringue"`

A directory with sources for "on-the-fly" generation.


### `MERINGUE_MKDOCS_CODE_PARCE_DOCS_PATH`

`default: "reference"`

Documentation directory for displaying "on-the-fly" generated source documentation.


### `MERINGUE_MKDOCS_CODE_PARCE_SHOW_NAV`

`default: false`

Parameter for debugging generated "on-the-fly" navigation.


### `MERINGUE_MKDOCS_ENABLED_GIT_REVISION_DATE`

`default: true`

Option to enable/disable modification dates for documentation files. It will be useful to disable it when developing locally so that the console is not clogged with errors.


### `MERINGUE_MKDOCS_OFFLINE`

`default: false`

Parameter for building documentation into a build working from a folder, without the need to start the server. read more about the mechanism [here](https://squidfunk.github.io/mkdocs-material/setup/building-for-offline-usage/).


### `MERINGUE_MKDOCS_ENABLE_MINIFY`

`default: true`

Parameter to enable plugin [minify](https://github.com/byrnereese/mkdocs-minify-plugin) minifying html, js and css when generating documentation.

When working with [local server][local-development] documentation, this option is disabled.


## Building and publishing

There is a separate `hatch run docs:build` command for building documentation.

But before pushing the updated documentation, please run the `hatch run docs:build-check` command, it will build the documentation and check the links for broken ones.

Documentation is collected in [GitHub Actions](https://docs.github.com/en/actions) and uploaded to the [gh-pages](https://github.com/dd/Meringue/tree/gh-pages) branch and published using [GitHub Pages](https://pages.github.com/).

The documentation is automatically collected and rolled out when pushing the release tag (`v*`), and when pushing to the `dev` branch, the dev version of the documentation is updated.
You can learn more about these processes in the [releasel](https://github.com/dd/Meringue/blob/master/.github/workflows/mkdocs-release.yml) and [dev](https://github.com/dd/Meringue/blob/master/.github/workflows/mkdocs-dev.yml) workflow configs.
