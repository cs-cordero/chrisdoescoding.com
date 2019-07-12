from typing import Generic, TypeVar

from django.db.models import QuerySet

T = TypeVar("T")

class BaseManager: ...
class Manager(BaseManager): ...
