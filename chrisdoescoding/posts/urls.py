from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from chrisdoescoding.posts import views

urlpatterns = [
    path('latest/', views.LatestPostView.as_view(), name='latest'),
    path('<int:pk>/', views.PostView.as_view(), name='post'),
    path('random/', views.RandomPostView.as_view(), name='random'),
    path('', views.AllPostsView.as_view(), name='list'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
