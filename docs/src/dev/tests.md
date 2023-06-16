# Tests

The project uses [pytest](https://docs.pytest.org/) for testing, and has set up coverage tests using [pytest-cov](https://pytest-cov.readthedocs.io/).

You can run tests in a development environment with the following command:

```console
$ hatch run test_check
```

A matrix for a set of python and django versions is also configured in hatch, you can see more about this in the settings in the `pyproject.toml` file, you can run the entire test matrix with the hatch script:

```console
$ hatch run test:check
```
