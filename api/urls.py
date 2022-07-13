from django.urls import path
from .views import (
    get_users, 
    add_user,
    delete_user,
)


urlpatterns = [
    path('users', get_users, name='get-users'),
    path('add_user', add_user, name='add-user'),
    path('delete_user/<str:user_id>', delete_user, name='delete-user'),
]
