# Meringue core

This is a basic package that contains a variety of general purpose functionality such as abstract models, various handlers, utilities, and more.


## Mixins

### CMTimeMixin

A primitive abstract model that adds the _ctime_ and _mtime_ fields to your model.


### SortingMixin

An abstract model that adds a sortable field, as well as a manager with sorting correction functionality.


#### correction_sorting

::: meringue.core.query.SortingQuerySet.correction_sorting
	options:
		show_root_heading: false
		show_root_toc_entry: false
		show_source: false


### PublicationMixin

::: meringue.core.models.PublicationMixin
	options:
		show_root_heading: false
		show_root_toc_entry: false
		show_source: false
		show_bases: false


#### published

::: meringue.core.query.PublicationQuerySet.published
	options:
		show_root_heading: false
		show_root_toc_entry: false
		show_source: false


#### unpublished

::: meringue.core.query.PublicationQuerySet.unpublished
	options:
		show_root_heading: false
		show_root_toc_entry: false
		show_source: false


### PublicationDatesMixin

::: meringue.core.models.PublicationDatesMixin
	options:
		show_root_heading: false
		show_root_toc_entry: false
		show_source: false
		show_bases: false


#### published

::: meringue.core.query.PublicationDatesQuerySet.published
	options:
		show_root_heading: false
		show_root_toc_entry: false
		show_source: false


#### unpublished

::: meringue.core.query.PublicationDatesQuerySet.unpublished
	options:
		show_root_heading: false
		show_root_toc_entry: false
		show_source: false


## Utils


### format_date_from_to

::: meringue.core.utils.datetime.format_date_from_to
	options:
		show_root_heading: false
		show_root_toc_entry: false
		show_source: false


## Templatetags


### cop_year

::: meringue.core.templatetags.meringue_base.cop_year
	options:
		show_root_heading: false
		show_root_toc_entry: false
		show_source: false


### date_range

::: meringue.core.templatetags.meringue_base.date_range
	options:
		show_root_heading: false
		show_root_toc_entry: false
		show_source: false


## Views


### im_a_teapot

::: meringue.core.views.im_a_teapot
	options:
		show_root_heading: false
		show_root_toc_entry: false
		show_source: false
