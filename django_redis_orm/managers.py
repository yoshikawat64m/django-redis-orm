from .redis import RedisClient


class BaseCacheManager:
    client = RedisClient()

    def __init__(self, model):
        self.model = model

    def delete(self, **attrs):
        instance = self.model(**attrs)
        self.client.delete(instance.key)


class TextCacheManager(BaseCacheManager):

    def get(self, **attrs):
        instance = self.model(**attrs)
        instance.text = self.client.get(instance.key)
        return instance


class ListCacheManager(BaseCacheManager):

    def get(self, **attrs):
        instance = self.model(**attrs)
        instance.items = self.client.get_list(instance.key)
        return instance
