from django.urls import path

from chrisdoescoding.posts import views

urlpatterns = [
    path('<int:pk>/', views.PostView.as_view(), name='post'),
]
