import threading


class _Global(threading.local):
    example_attr: str = None


_global = _Global()


class _GlobalProxy:
    attr = None

    def __init_subclass__(cls, **kwargs):
        assert hasattr(_global, cls.attr)

    @classmethod
    def set(cls, data):
        setattr(_global, cls.attr, data)

    @classmethod
    def get(cls):
        return getattr(_global, cls.attr)

    def __init__(self, data):
        self.set(data)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.set(None)


class ExampleAttr(_GlobalProxy):
    attr = "example_attr"
