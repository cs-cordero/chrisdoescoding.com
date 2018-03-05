from django.urls import path

from chrisdoescoding.posts import views

urlpatterns = [
    path('latest/', views.LatestPostView.as_view(), name='latest'),
    path('<int:pk>/', views.PostView.as_view(), name='post'),
    path('', views.AllPostsView.as_view(), name='list'),
]
