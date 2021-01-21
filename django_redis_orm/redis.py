import json
from django_redis import get_redis_connection


class RedisClient:

    def __init__(self, name='default'):
        self.conn = get_redis_connection(name)

    def exists(self, key):
        value = self.conn.get(key)
        return value is not None

    def get(self, key, decode_type="utf-8"):
        value = self.conn.get(key)
        if value is None:
            return ''
        else:
            return value.decode(decode_type)

    def get_type(self, field):
        return self.conn.type(field).decode()

    def get_list(self, list_field, json_decode=True):
        if self.get_type(list_field) == 'list':
            byte_list = self.conn.lrange(list_field, 0, -1)
            if json_decode:
                return list(map(lambda v: self._json_decode(v.decode()), byte_list))
            else:
                return list(map(lambda v: v.decode(), byte_list))
        else:
            return []

    def push_list(self, list_field, new_val, json_encode=True):
        if self.get_type(list_field) != 'list':
            self.conn.delete(list_field)

        if json_encode:
            new_val = self._json_encode(new_val)
        self.conn.rpush(list_field, new_val)

    def trim_list(self, field, i1, i2):
        self.conn.ltrim(field, i1, i2)

    def set(self, field, text, exp=None):
        if exp:
            self.conn.set(field, text, exp)
        else:
            self.conn.set(field, text)

    def delete(self, field):
        self.conn.delete(field)

    def _json_encode(self, val_dict):
        return json.dumps(val_dict, indent=2, ensure_ascii=False)

    def _json_decode(self, val_string):
        return json.loads(val_string)
