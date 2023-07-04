# Getting Started


## Installation

```console
$ pip install meringue
```


## Configuration

You can connect individual modules as needed (read more in the documentation of the corresponding module):

```pycon
INSTALLED_APPS = (
    ...
    'meringue.core',
    ...
)
```


All settings for the library are specified inside the `MERINGUE` parameter (for more details, see the corresponding [section](./conf.md)):

```pycon
MERINGUE = {
    ...
}
```
