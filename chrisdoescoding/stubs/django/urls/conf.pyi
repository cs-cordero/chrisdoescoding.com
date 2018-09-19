from django.http import HttpRequest, HttpResponse
from django.urls.resolvers import RoutePattern

from functools import partial
from typing import Any, Union, Tuple, Callable


def include(arg: Union[str, Tuple[str, str]], namespace: str) -> Any: ...

def _path(route: str, view: Callable[[HttpRequest], HttpResponse],
          kwargs: Any = None, name: str = None, Pattern: Any = None):

path = partial(_path, Pattern=RoutePattern)
