from django.urls import path

from cards import views

urlpatterns = [
    path('cards/', views.ListCard.as_view(), name='list_card'),
    path('add-card/', views.AddCard.as_view(), name='add_card'),
    path('card/<int:pk>/', views.DetailCard.as_view(), name='detail_card'),
    path('', views.home, name='home')
]