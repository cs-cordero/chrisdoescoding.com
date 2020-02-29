from typing import Any, Callable, Dict

from django.http import HttpRequest, HttpResponse

class ContextMixin: ...

class TemplateResponseMixin:
    def render_to_response(
        self, context: Dict[str, Any], **response_kwargs: Any
    ) -> HttpResponse: ...

class View:
    @classmethod
    def as_view(cls, **initkwargs: Any) -> Callable[..., HttpResponse]: ...

class TemplateView(TemplateResponseMixin, ContextMixin, View): ...
class RedirectView(View): ...
