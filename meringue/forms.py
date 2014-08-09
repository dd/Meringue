# -*- coding:utf-8 -*-

from django.forms.formsets import DEFAULT_MAX_NUM, BaseFormSet


class RequiredFormSet(BaseFormSet):

    def __init__(self, *args, **kwargs):
        super(RequiredFormSet, self).__init__(*args, **kwargs)
        for form in self.forms:
            form.empty_permitted = False


def required_formset_factory(form, formset=RequiredFormSet, extra=1, can_order=False,
                    can_delete=False, max_num=None, validate_max=False):
    """
    полная копия стандартной джанговской функции, за исключением того что
    переопределена стандартная функция набора форм, просто что бы не париться с
    этим каждый раз
    """
    if max_num is None:
        max_num = DEFAULT_MAX_NUM
    absolute_max = max_num + DEFAULT_MAX_NUM
    attrs = {'form': form, 'extra': extra,
             'can_order': can_order, 'can_delete': can_delete,
             'max_num': max_num, 'absolute_max': absolute_max,
             'validate_max' : validate_max}
    return type(form.__name__ + str('FormSet'), (formset,), attrs)
