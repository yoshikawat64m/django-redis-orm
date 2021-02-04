from .base import BaseCache, BaseCacheMeta
from .managers import TextCacheManager, ListCacheManager


class TextCache(BaseCache, metaclass=BaseCacheMeta):
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

    ExampleText.objects.delete(organization_id=1)
    ExampleText.objects.exists(organization_id=1) => False
    instance = ExampleText.objects.get(organization_id=1)
    instance.text => ''
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
        self.client.set(self.key, self.text, exp)
        self.clear_text()


class ListCache(BaseCache, metaclass=BaseCacheMeta):
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
        self._queries = []
        super().__init__(**attrs)

    @property
    def items(self):
        if self._items is None:
            self._items = self.client.get_list(self.key)
        return self._items

    @property
    def queries(self):
        return self._queries

    def add_query(self, item):
        self._queries.append(item)

    def clear_queries(self):
        self._queries = []

    def clear_items(self):
        self._items = None

    def push(self, item):
        self.add_query(('push', item))

    def trim(self, i1, i2):
        self.add_query(('trim', i1, i2))

    def save(self, exp=None):
        for query in self.queries:
            if query[0] == 'push':
                self.client.push_list(self.key, query[1])
            elif query[0] == 'trim':
                self.client.trim_list(self.key, query[1], query[2])

        self.clear_items()
        self.clear_queries()
