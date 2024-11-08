from django.urls import path

from cards import views

urlpatterns = [
    path('cards/', views.CardList.as_view(), name='card_list'),
    path('card-add/', views.CardAdd.as_view(), name='card_add'),
    path('card/<int:pk>/', views.CardDetail.as_view(), name='card_detail'),
    path('card-delete/<int:pk>/', views.CardDelete.as_view(), name='card_delete'),
    path('card-edit/<int:pk>/', views.CardUpdate.as_view(), name='card_edit'),

    path('departure-add/<int:pk>/', views.DepartureAdd.as_view(), name='departure_add'),
    path('departure/<int:pk>/', views.DepartureDetail.as_view(), name='departure_detail'),
    path('', views.home, name='home')
]
