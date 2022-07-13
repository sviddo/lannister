from rest_framework.decorators import api_view
from .models import (
    User, 
    UserRole, 
)
from rest_framework.response import Response
from rest_framework import status



@api_view(['GET'])
def get_users(requests):
    users = User.objects.all()
    if users:
        users_with_roles = []
        for user in users:
            service_id = user.service_id
            roles = []
            for user_role in UserRole.objects.filter(user=service_id):
                roles.append(user_role.role.name)

            users_with_roles.append({'service_id': service_id, 'roles': roles})
        return Response(users_with_roles, status=status.HTTP_200_OK)
    else:
        return Response(["No users!"], status=status.HTTP_404_NOT_FOUND)