from django.urls import path

from card import views

urlpatterns = [
    path('', views.test, name='test')
]