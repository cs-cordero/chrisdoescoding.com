from functools import partial
from typing import Any, Callable, Optional, Tuple, Union

from django.http import HttpRequest, HttpResponse
from django.urls.resolvers import RoutePattern, URLPattern, URLResolver

def include(arg: Union[str, Tuple[str, str]], namespace: str) -> Any: ...
def path(
    route: str,
    view: Callable[..., HttpResponse],
    kwargs: Any = None,
    name: Optional[str] = None,
) -> Union[URLPattern, URLResolver]: ...
