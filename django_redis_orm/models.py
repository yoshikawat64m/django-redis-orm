from .base import BaseCache
from .managers import TextCacheManager, ListCacheManager


class TextCache(BaseCache):
    """
    Usage
    class ExampleText(TextCache):
        name = 'example'
        attrs = [
            'organization_id'
        ]

    instance = ExampleText(organization_id=1)
    instance.text = 'test'
    instance.save()
    instance.text => 'test'

    instance = ExampleText.objects.get(organization_id=1)
    instance.text => 'test'
    """
    manager = TextCacheManager

    def __init__(self, **attrs):
        self._text = None
        super().__init__(**attrs)

    @property
    def text(self):
        if self._text is None:
            self._text = self.client.get(self.key)
        return self._text

    @text.setter
    def text(self, text):
        assert type(text) is str
        self._text = text

    def clear_text(self):
        self._text = None

    def save(self, exp=None):
        assert type(self._text) is str
        self.client.set(self.key, self._text, exp)
        self.clear_text()


class ListCache(BaseCache):
    """
    Usage
    class ExampleList(ListCache):
        name = 'example'
        attrs = [
            'organization_id'
        ]

    instance = ExampleList(organization_id=1)
    instance.push('v1')
    instance.push('v2')
    instance.items => ['v1', 'v2']

    instance = ExampleList.objects.get(organization_id=1)
    instance.items => ['v1', 'v2']
    """
    manager = ListCacheManager

    def __init__(self, **attrs):
        self._items = None
        super().__init__(**attrs)

    @property
    def items(self):
        if self._items is None:
            self._items = self.client.get_list(self.key)
        return self._items

    @items.setter
    def items(self, items):
        assert type(items) is list
        self._items = items

    def clear_items(self):
        self._items = None

    def push(self, item):
        self.client.push_list(self.key, item)
        self.clear_items()

    def trim(self, i1, i2):
        self.client.trim_list(self.key, i1, i2)
        self.clear_items()

    def save(self, exp=None):
        assert type(self._items) is list
        self.client.set(self.key, self._items, exp)
        self.clear_items()
