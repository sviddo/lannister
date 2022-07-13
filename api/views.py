import json
import rest_framework.serializers as ser
import django.core.exceptions as exceptions
from rest_framework.decorators import api_view
from requests import JSONDecodeError
from .models import (
    User, 
    UserRole, 
)
from rest_framework.views import APIView
from .serializers import (
    UserSerializer,
    UserRoleSerializer,
)
from rest_framework.response import Response
from rest_framework import status
from json.decoder import JSONDecodeError



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



@api_view(['POST'])
def add_user(request):
    try:
        user_to_add = json.loads(request.body)
    except JSONDecodeError:
        return Response(["Invalid json format! Please, check its correctness"], status=status.HTTP_400_BAD_REQUEST)

    user_serializer = UserSerializer(data=user_to_add)
    user_role_serializer = UserRoleSerializer(data=user_to_add)

    try:
        if user_serializer.is_valid():
            pass
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if user_role_serializer.is_valid():
            user_serializer.save()
            user_role_serializer.save()
        else:
            return Response(user_role_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except ser.ValidationError as exc:
        exception_message = exc.message
        return Response([exception_message], status=status.HTTP_400_BAD_REQUEST)

    except exceptions.ValidationError as exc:
        exception_message = exc.message
        return Response([exception_message], status=status.HTTP_400_BAD_REQUEST)

    return Response(data=user_to_add, status=status.HTTP_200_OK)



@api_view(['DELETE'])
def delete_user(request, user_id):
    user_to_delete = User.objects.filter(service_id=user_id).first()
    if user_to_delete:
        return Response(user_to_delete.delete(), status=status.HTTP_200_OK)
    return Response(["No such user!"], status=status.HTTP_400_BAD_REQUEST)