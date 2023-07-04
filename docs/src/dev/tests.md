# Tests

The project uses [pytest](https://docs.pytest.org/) for testing, as well as set up coverage tests using [pytest-cov](https://pytest-cov.readthedocs.io/), it is highly recommended for review.


## Usage

You can run tests in a development environment with the following command:

```console
$ hatch run test:check
```

A matrix for a set of python and django versions is also configured in hatch, you can see more about this in the settings in the `pyproject.toml` file, you can run the entire test matrix with the hatch script:

```console
$ hatch run mtest:check
```


## Development

When developing tests, you may need to create new migrations, this can be done with the following command

```console
$ hatch run test:makemigrations
```

The application used in the tests lies in the `test_project` directory.

The database is used by in-memory SQLite.


## Autotests

Tests are automatically processed when pushing to `master` and release branches `release/*`. See workflow [config](https://github.com/dd/Meringue/blob/master/.github/workflows/test.yml) for details.

In the process, test results are uploaded to [codecov.io](https://app.codecov.io/gh/dd/Meringue).
