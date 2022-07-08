from django.urls import path

from .views import get_users, add_users

urlpatterns = [
    path('users/', get_users, name='get-users'),
    path('add_users/', add_users, name='add-users'),
]
