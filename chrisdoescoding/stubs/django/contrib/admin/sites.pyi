from typing import Any

from django.db.models import Model
from django.utils.functional import LazyObject

class DefaultAdminSite(LazyObject):
    def _setup(self) -> Any: ...
    # hardcoded for ease-of-typing
    def register(self, *args: Any, **kwargs: Any) -> Any: ...

site = DefaultAdminSite()
