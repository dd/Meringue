# Meringue core

This is a basic package that contains a variety of general purpose functionality such as abstract models, various handlers, utilities, and more.


## Mixins

### `CMTimeMixin`

[code][meringue.core.models.CMTimeMixin]

A primitive abstract model that adds the _ctime_ and _mtime_ fields to your model.


### `SortingMixin`

[code][meringue.core.models.SortingMixin]

An abstract model that adds a sortable field, as well as a manager with sorting correction functionality.


#### `correction_sorting`

::: meringue.core.query.SortingQuerySet.correction_sorting
	options:
		show_root_heading: false
		show_root_toc_entry: false
		show_source: false


### `PublicationMixin`

[code][meringue.core.models.PublicationMixin]


### `PublicationDatesMixin`

[code][meringue.core.models.PublicationDatesMixin]

