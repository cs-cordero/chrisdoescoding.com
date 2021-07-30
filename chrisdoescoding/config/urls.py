"""chrisdoescoding URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

kb_patterns = [
    # The Knowledge Base (Kb) is served by Nginx, everything is static.
    # If Nginx is mis-configured, then this route will get hit.
    # This is an error, just redirect to home.
    path("", RedirectView.as_view(pattern_name="home"), name="kb"),
]

urlpatterns = [
    path("", RedirectView.as_view(url="/posts/latest"), name="home"),
    path("posts/", include("posts.urls")),
    path("acnh/", include("acnh.urls")),
    path("admin/", admin.site.urls),
    path("kb/", include(kb_patterns)),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  # type: ignore
