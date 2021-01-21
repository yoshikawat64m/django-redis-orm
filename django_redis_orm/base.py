from abc import ABCMeta, abstractmethod
from .exceptions import AttributeNotDefined, AttributeNotSet


class BaseCacheMeta(ABCMeta):
    def __init__(cls, name, bases, name_space):
        cls.set_objects()
        super().__init__(name, bases, name_space)


class BaseCache(metaclass=BaseCacheMeta):
    name = None
    attrs = []

    def __init__(self, **attrs):
        # set attributes in instance
        for attrname, attrvalue in attrs.items():
            if attrname not in self.attrs:
                raise AttributeNotDefined('Attribute %s is not defined.' % attrname)
            setattr(self, attrname, attrvalue)

    @property
    def key(self):
        key = self.name
        for attrname in self.attrs:
            attrvalue = getattr(self, attrname, '')
            if not attrvalue:
                raise AttributeNotSet('Attribute %s is not set.' % attrname)
            key += '_' + str(attrvalue)
        return key

    @property
    def client(self):
        return self.objects.client

    @classmethod
    def set_objects(cls):
        cls.objects = cls.manager(cls)

    def delete(self):
        self.client.delete(self.key)
