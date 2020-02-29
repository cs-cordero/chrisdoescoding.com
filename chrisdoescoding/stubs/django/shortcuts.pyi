from typing import Any, Dict, Optional

from django.http import HttpRequest, HttpResponse

def render(
    request: HttpRequest,
    template_name: str,
    context: Optional[Dict[str, Any]] = None,
    content_type: Any = None,
    status: Any = None,
    using: Any = None,
) -> HttpResponse: ...
