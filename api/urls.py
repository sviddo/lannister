from django.urls import path
from .views import (get_users, add_user)


urlpatterns = [
    path('users', get_users, name='get-users'),
    path('add_user', add_user, name='add-user'),
]