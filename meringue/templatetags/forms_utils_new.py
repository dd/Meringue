# -*- coding: utf-8 -*-

import logging
import re

from django import forms
from django import template
from django.utils.safestring import mark_safe


register = template.Library()

def get_name(field):
    caption = field.widget.__class__.__name__
    r = ur'([A-Z]{1})([a-z]+)'
    p = re.compile(r)
    caption = p.sub(lambda m: '_'+m.group().lower(), caption)
    return caption


@register.filter
def field_render_classes(boundfield):
    """
        выводит список параметров через пробел
            required - если обязательное поле
            errors - если есть ошибки
            valid - если валидное
            meringue-<field_name> - идентификатор
    """

    result = ''
    if boundfield.field.required:
        result += ' required'
    if boundfield.errors:
        result += ' errors'
    if not boundfield.errors and boundfield.form.errors and boundfield.value:
        result += ' valid'
    result += ' meringue-'+get_name(boundfield.field)[1:]
    return result


class FieldRender(object):

    def __init__(self, boundfield):
        self.field = boundfield
        self.caption = get_name(boundfield.field)

    def render(self):
        result = getattr(self, self.caption+'_render', self._default_with_label_render)
        return result()

    # def _default_render(self):
    #     return self.field

    def _default_with_label_render(self):
        result = u'<label for=\"id_%s\" >%s</label>%s' % (
            self.field.html_name,
            unicode(self.field.label),
            self.field
        )
        return mark_safe(result)

    # def _customize_select_render(self):
    #     return self._default_with_label_render()

    # def _input_with_label_render(self):
    #     return self._default_with_label_render()

    # def _checkbox_select_multiple_render(self):
    #     return self._default_with_label_render()

    # def _custom_range_slider_render(self):
    #     return self._default_with_label_render()

    # def _checkbox_input_render(self):
    #     result = u'%s<label for=\"id_%s\" >%s</label>' % (
    #         self.field,
    #         self.field.html_name,
    #         unicode(self.field.label),
    #     )
    #     return mark_safe(result)


@register.filter
def field_render(boundfield):
    """
        Рендерит поле в соответствии с правилами
    """

    result = FieldRender(boundfield)
    return result.render()
