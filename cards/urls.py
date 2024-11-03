from django.urls import path

from cards import views

urlpatterns = [
    path('cards/', views.ListCard.as_view(), name='list_card'),
    path('add-card/', views.AddCard.as_view(), name='add_card'),
    path('card/<int:pk>/', views.DetailCard.as_view(), name='detail_card'),
    path('edit-card/<int:pk>/', views.UpdateCard.as_view(), name='edit_card'),

    path('add-departure/<int:pk>/', views.AddDeparture.as_view(), name='add_departure'),

    path('', views.home, name='home')
]
