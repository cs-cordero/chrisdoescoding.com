from django.utils.functional import LazyObject

from typing import Any


class LazySettings(LazyObject):
    def __getattribute__(self, name: str) -> Any: ...

settings = LazySettings()
