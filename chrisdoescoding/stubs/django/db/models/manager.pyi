from django.db.models import QuerySet

from typing import Generic, TypeVar

T = TypeVar('T')

class BaseManager: ...
class Manager(BaseManager, QuerySet[T], Generic[T]): ...
