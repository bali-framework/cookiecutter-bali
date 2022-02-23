import json
from datetime import timedelta
from threading import RLock
from typing import Any, Callable, NamedTuple, Optional

from loguru import logger
from redis import RedisError

from conf import redis_cli, settings

__all__ = ["redis_property", "DEFAULT_EX"]


class Cache(NamedTuple):
    read: Callable[[str], Optional[str]]
    write: Callable[[str, str], Any]
    remove: Callable[[str], Any]


DEFAULT_EX = timedelta(days=1)
catch_redis_error = logger.catch(RedisError)


class redis_property:  # noqa
    """
    每个属性仅计算一次然后序列化缓存至 redis，仅当键不存在时缓存。
    将 ex 设置为秒数或者 timedelta 对象表示多长时间后过期，默认为一天。
    当 ex 被设置为 None 时，将永久缓存。
    """

    def __init__(self, ex=DEFAULT_EX):
        if callable(ex):
            self.func, self.ex = ex, None
        else:
            self.func, self.ex = None, ex

        self.lock = RLock()

    def __call__(self, func):
        self.func = func
        return self

    def __set_name__(self, *_):
        for member_name in [
            "__doc__",
            "__name__",
            "__module__",
        ]:
            value = getattr(self.func, member_name)
            setattr(self, member_name, value)

    def __get__(self, instance, _):
        if instance is None:
            return self

        cache, key = self._get_cache(), self._get_key(instance)
        value = cache.read(key)
        if value is not None:
            return self._loads(value)

        with self.lock:
            value = cache.read(key)
            if value is not None:
                return self._loads(value)

            value = self.func(instance)
            cache.write(key, self._dumps(value))
            return value

    def __delete__(self, instance):
        cache, key = self._get_cache(), self._get_key(instance)
        cache.remove(key)

    _dumps = staticmethod(json.dumps)
    _loads = staticmethod(json.loads)

    def _get_key(self, instance):
        instance_name, func_name = type(instance).__name__, self.func.__name__
        return f"{settings.TITLE}:{instance_name}:id:{instance.id}:{func_name}"

    def _get_cache(self):
        @catch_redis_error
        def read(key):
            value = redis_cli.get(key)
            if value is None:
                return

            return value.decode("utf-8")

        @catch_redis_error
        def write(key, value):
            return redis_cli.set(key, value, ex=self.ex, nx=True)

        @catch_redis_error
        def remove(key):
            return redis_cli.delete(key)

        return Cache(read=read, write=write, remove=remove)
