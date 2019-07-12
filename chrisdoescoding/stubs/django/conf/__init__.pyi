from typing import Any

from django.utils.functional import LazyObject

class LazySettings(LazyObject):
    def __getattribute__(self, name: str) -> Any: ...

settings = LazySettings()
