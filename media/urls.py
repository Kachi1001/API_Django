from django.urls import path
from . import views

urlpatterns = [
    path('get', views.get),
    path('register', views.register),
]