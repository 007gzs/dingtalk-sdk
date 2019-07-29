# encoding: utf-8
from __future__ import absolute_import, unicode_literals

import random
import string


class FieldBase(object):
    component_name = None

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            if callable(v):
                v = v()
            setattr(self, k, v)
        if getattr(kwargs, 'id', None) is None:
            self.id = self.gen_id()

    def gen_id(self):
        return "%s-%s" % (self.component_name, random.sample(string.ascii_uppercase + string.digits, 8))

    def get_dict(self):
        assert self.component_name
        return {'component_name': self.component_name, "props": self.get_data()}

    def get_data(self):
        ret = {}
        for k in dir(self):
            if k.startswith('_') or k == 'component_name':
                continue
            v = getattr(self, k, None)
            if v is None or hasattr(v, '__call__'):
                continue
            if v is not None:
                if isinstance(v, FieldBase):
                    v = v.get_data()
                ret[k] = v
        return ret


class TextField(FieldBase):
    component_name = "TextField"

    def __init__(self, label, required=True, placeholder='', **kwargs):
        """

        :param label: 表单组件名称
        :param required: 是否必填
        :param placeholder: 输入提示
        :param kwargs:
        """
        super(TextField, self).__init__(required=required, placeholder=placeholder, label=label, **kwargs)


class TextareaField(FieldBase):
    component_name = "TextareaField"

    def __init__(self, label, required=True, placeholder='', **kwargs):
        """

        :param label: 表单组件名称
        :param required: 是否必填
        :param placeholder: 输入提示
        :param kwargs:
        """
        super(TextareaField, self).__init__(required=required, placeholder=placeholder, label=label, **kwargs)


class MoneyField(FieldBase):
    component_name = "MoneyField"

    def __init__(self, label, required=True, placeholder='', not_upper='', **kwargs):
        """

        :param label: 表单组件名称
        :param required: 是否必填
        :param placeholder: 输入提示
        :param kwargs:
        """
        super(MoneyField, self).__init__(
            required=required, placeholder=placeholder, label=label, not_upper=not_upper, **kwargs
        )


class NumberField(FieldBase):
    component_name = "NumberField"

    def __init__(self, label, required=True, placeholder='', unit='', **kwargs):
        """

        :param label: 表单组件名称
        :param required: 是否必填
        :param placeholder: 输入提示
        :param kwargs:
        """
        super(NumberField, self).__init__(required=required, placeholder=placeholder, label=label, unit=unit, **kwargs)


class DDDateField(FieldBase):
    component_name = "DDDateField"

    def __init__(self, label, required=True, placeholder='', unit='', **kwargs):
        """

        :param label: 表单组件名称
        :param required: 是否必填
        :param placeholder: 输入提示
        :param kwargs:
        """
        super(DDDateField, self).__init__(required=required, placeholder=placeholder, label=label, unit=unit, **kwargs)


class DDDateRangeField(FieldBase):
    component_name = "DDDateRangeField"

    def __init__(self, label, required=True, placeholder='', unit='', **kwargs):
        """

        :param label: 表单组件名称
        :param required: 是否必填
        :param placeholder: 输入提示
        :param kwargs:
        """
        super(DDDateRangeField, self).__init__(
            required=required, placeholder=placeholder, label=label, unit=unit, **kwargs
        )
