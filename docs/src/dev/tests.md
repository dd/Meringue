# Tests

In its simplest form, running the tests would look like this:

```console
$ hatch run test:check
```

This command will run tests one by one for all [matrix](https://hatch.pypa.io/latest/config/environment/advanced/#matrix) possible python and django matches supported by the project (A current list can be found in `pyproject.toml` project).

During development, this may be redundant, and it may be necessary to run tests for only one match from the matrix, this can be done as follows:

```console
$ hatch run test.py3.11-4.0:check
```

This command will run tests for python 3.11 and django 4.0, you can read more about how it works in the documentation [hatch](https://hatch.pypa.io/latest/cli/reference/#hatch-env-run).
