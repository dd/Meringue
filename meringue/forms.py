# -*- coding:utf-8 -*-

from django import forms


class form_fieldsets(object):
    '''
        mixin разбивает форму на несколько групп
        группы указываются в виде списка в Meta.fieldsets.
        элементы списка - словари с ключами fields и title, содержащие список
        полей и название группы соответственно
    '''

    def fieldsets(self):
        fieldsets = getattr(self.Meta, 'fieldsets', [{'fields': self.fields.keys(), 'title': 'main'}])
        result = list()
        for fieldset in fieldsets:
            result.append({
                'fields': [forms.forms.BoundField(self, self.fields[f], f)
                           for f in fieldset['fields'] if f in self.fields],
                'title': fieldset['title']
            })
        return result


class BaseFormSet(forms.BaseFormSet):
    """
        добавил возможность указать префикс для всего набора форм включая
        управляющие поля
    """
    def __init__(self, *args, **kwargs):
        prefix = self.prefix
        super(BaseFormSet, self).__init__(*args, **kwargs)
        if prefix:
            self.prefix = prefix


def formset_factory(form, formset=BaseFormSet, extra=1, can_order=False,
                    can_delete=False, max_num=None, validate_max=False,
                    min_num=None, validate_min=False, prefix=None):
    """
        помимо всего передаём префикс
    """
    if min_num is None:
        min_num = forms.formsets.DEFAULT_MIN_NUM
    if max_num is None:
        max_num = forms.formsets.DEFAULT_MAX_NUM
    # hard limit on forms instantiated, to prevent memory-exhaustion attacks
    # limit is simply max_num + DEFAULT_MAX_NUM (which is 2*DEFAULT_MAX_NUM
    # if max_num is None in the first place)
    absolute_max = max_num + forms.formsets.DEFAULT_MAX_NUM
    attrs = {'form': form, 'extra': extra,
             'can_order': can_order, 'can_delete': can_delete,
             'min_num': min_num, 'max_num': max_num,
             'absolute_max': absolute_max, 'validate_min': validate_min,
             'validate_max': validate_max, 'prefix': prefix}
    return type(form.__name__ + str('FormSet'), (formset,), attrs)
