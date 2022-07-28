from django.urls import path
from .views import (
    get_users, 
    SingleUser,
    add_user,
    ReviewerRole,
    get_requests,
    create_request,
    RequestView,
    get_user_requests,
    get_requests_history,
    get_requests_per_reviewer,
)

urlpatterns = [
    path('users', get_users, name='get-users'),
    path('user/<str:user_id>', SingleUser.as_view(), name='single-user'),
    path('add_user', add_user, name='add-user'),
    path('reviewer_role/<str:user_id>', ReviewerRole.as_view(), name='reviewer-role'),  # add/remove reviewer role
    path('requests', get_requests, name='all-requests'),  # get all requests (use case for admin)
    path('create_request', create_request, name='create-request'),
    path('request/<str:request_id>', RequestView.as_view(), name='manage-request'),  # update/delete request
    path('requests/<str:user_id>', get_user_requests, name='requests-per-user'),
    path('requests_history', get_requests_history, name='request-history'),
    path('reviewer_requests/<str:reviewer_id>', get_requests_per_reviewer, name='requests-per-reviewer'),
]
