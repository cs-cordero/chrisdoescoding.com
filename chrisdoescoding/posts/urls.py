from django.urls import path

from chrisdoescoding.posts import views

from typing import List, Union

foo = views.LatestPostView.as_view()
urlpatterns = [
    path('latest/', views.LatestPostView.as_view(), name='latest'),
    path('<int:pk>/', views.PostView.as_view(), name='post'),
    path('random/', views.RandomPostView.as_view(), name='random'),
    path('', views.AllPostsView.as_view(), name='list'),
]
