from django.urls import path

from chrisdoescoding.southpark import views

urlpatterns = [
    path('random/', views.SouthParkRedirectView.as_view(), name='southpark_redirect'),
    path('', views.SouthParkView.as_view(), name='southpark'),
]
