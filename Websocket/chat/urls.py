from django.urls import path

from . import views

urlpatterns = [
    path('chatadmin/', views.index_view_admin, name='chat-index-admin'),
    path('chatuser/', views.index_view_user, name='chat-index-user'),
    path('<str:room_name>/', views.room_view_admin, name='chat-room-admin'), 
    path('room-create/<str:room_name>/', views.room_view_user, name='chat-roomuser'),
]