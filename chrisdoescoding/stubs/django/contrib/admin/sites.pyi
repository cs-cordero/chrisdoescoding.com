from django.db.models import Model
from django.utils.functional import LazyObject

from typing import Any


class DefaultAdminSite(LazyObject):
    def _setup(self) -> Any: ...

    # hardcoded for ease-of-typing
    def register(self, *args: Any, **kwargs: Any) -> Any: ...

site = DefaultAdminSite()
