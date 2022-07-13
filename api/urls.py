from django.urls import path
from .views import (
    get_users, 
    add_user, 
    delete_user, 
    RequestView, 
    get_user_requests, 
    get_requests, 
    create_request,
    ReviewerRole,
)


urlpatterns = [
    path('users', get_users, name='get-users'),
    path('add_user', add_user, name='add-users'),
    path('delete_user/<str:user_id>', delete_user, name='delete-user'),
    path('reviewer_role/<str:user_id>', ReviewerRole.as_view(), name='reviewer-role'),  # add/remove reviewer role
    path('requests', get_requests, name='all-requests'),  # get all requests (use case for admin)
    path('create_request', create_request, name='create-request'),
    path('request/<request_id>', RequestView.as_view(), name='manage-request'),  # update/delete request
    path('requests/<str:user_id>', get_user_requests, name='requests-per-user'),
]