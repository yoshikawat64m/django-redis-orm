from django.test import TestCase
from .models import TextCache, ListCache
from .exceptions import AttributeNotDefined, AttributeNotSet


class TextCacheExample(TextCache):
    name = 'example'
    attrs = [
        'user_id',
    ]


class ListCacheExample(ListCache):
    name = 'example'
    attrs = [
        'user_id',
    ]


class TextCacheTest(TestCase):

    def test_initialize(self):
        instance = TextCacheExample(user_id=1)
        self.assertTrue(instance.user_id == 1)

    def test_set_and_get(self):
        instance = TextCacheExample(user_id=1)
        instance.text = 'text'
        instance.save()

        instance2 = TextCacheExample.objects.get(user_id=1)

        self.assertTrue(instance.text == 'text')
        self.assertTrue(instance2.text == 'text')

    def test_get_blank(self):
        TextCacheExample.objects.delete(user_id=1)
        instance = TextCacheExample.objects.get(user_id=1)
        exists = TextCacheExample.objects.exists(user_id=1)

        self.assertTrue(instance.text == '')
        self.assertTrue(exists is False)

    def test_set_error(self):
        instance = TextCacheExample()
        try:
            instance.text = 'text'
            instance.save()
            raise Exception
        except Exception as err:
            self.assertTrue(type(err) is AttributeNotSet)


class ListCacheTest(TestCase):

    def test_initialize(self):
        instance = ListCacheExample(user_id=1)
        self.assertTrue(instance.user_id == 1)

    def test_push_and_get(self):
        ListCacheExample.objects.delete(user_id=1)
        instance = ListCacheExample(user_id=1)
        instance.push('item1')
        instance.push('item2')
        instance.save()
        self.assertTrue(instance.items == ['item1', 'item2'])

        instance2 = ListCacheExample.objects.get(user_id=1)

        self.assertTrue(instance.items == ['item1', 'item2'])
        self.assertTrue(instance2.items == ['item1', 'item2'])

    def test_get_blank(self):
        instance = ListCacheExample(user_id=1)
        instance.push('item1')
        instance.save()
        ListCacheExample.objects.delete(user_id=1)
        instance = ListCacheExample.objects.get(user_id=1)
        self.assertTrue(instance.items == [])
