import json
import rest_framework.serializers as ser
import django.core.exceptions as exceptions
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import api_view
from requests import JSONDecodeError
from .models import (
    User, 
    Role,
    UserRole, 
    Request,
)
from rest_framework.views import APIView
from .serializers import (
    UserSerializer,
    UserRoleSerializer,
    RequestSerializer,
)
from rest_framework.response import Response
from rest_framework import status
from json.decoder import JSONDecodeError


# @require_http_methods(['GET'])
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
        Response(["No users!"], status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
# @require_http_methods(['POST'])
def add_user(request):
    try:
        user_to_add = json.loads(request.body)
        print(user_to_add)

        user_serializer = UserSerializer(data=user_to_add)
        user_role_serializer = UserRoleSerializer(data=user_to_add)

        try:
            print(user_serializer.is_valid())
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

    except TypeError:
        return Response(["User data must be dictionary!"], status=status.HTTP_400_BAD_REQUEST)

    except JSONDecodeError:
        return Response(["Invalid json format! Please, check its correctness"], status=status.HTTP_400_BAD_REQUEST)
    print(type(user_to_add), user_to_add)
    return Response(data=user_to_add, status=status.HTTP_200_OK)



@require_http_methods(["DELETE"])
def delete_user(request, user_id):
    user_to_delete = User.objects.filter(service_id=user_id).first()
    if user_to_delete:
        return Response(user_to_delete.delete(), status=status.HTTP_200_OK)
    return Response(["No such user!"], status=status.HTTP_400_BAD_REQUEST)



class ReviewerRole(APIView):
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(["User does not exist!"], status=status.HTTP_400_BAD_REQUEST)


    def patch(self, request, user_id):
        user_to_update = self.get_object(user_id)
        if type(user_to_update) == Response:
            return user_to_update
        if UserRole.objects.filter(user=user_to_update, role=Role.objects.get(pk='r')).first():
            return Response(["User is already reviewer!"], status=status.HTTP_400_BAD_REQUEST)

        UserRole(user=user_to_update, role=Role.objects.get(pk='r')).save()

        return Response(self.get_user(user_id), status=status.HTTP_200_OK)


    def delete(self, request, user_id):
        user_to_update = self.get_object(user_id)
        if type(user_to_update) == Response:
            return user_to_update
        if not UserRole.objects.filter(user=user_id, role=Role.objects.get(pk='r')):
            return Response(["User is not reviewer!"], status=status.HTTP_400_BAD_REQUEST)

        UserRole.objects.get(user=user_to_update, role=Role.objects.get(pk='r')).delete()

        return Response(self.get_user(user_id), status=status.HTTP_200_OK)


    @staticmethod
    def get_user(user_id):
        users_with_roles = []
        roles = []
        for user_role in UserRole.objects.filter(user=user_id):
            roles.append(user_role.role.name)

        users_with_roles.append({'service_id': user_id, 'roles': roles})

        return users_with_roles




@require_http_methods(["GET"])
def get_requests(request):
    requests = Request.objects.all()
    if requests:
        serializer = RequestSerializer(requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(["No requests created"], status=status.HTTP_400_BAD_REQUEST)



@require_http_methods(["POST"])
def create_request(request):
    try:        
        new_request = json.loads(request.body)
        if Request.objects.filter(**new_request).first():
            return Response(["Such request is already exist!"], status=status.HTTP_400_BAD_REQUEST)
        serializer = RequestSerializer(data=new_request)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except JSONDecodeError:
        return Response(["Invalid json format! Please, check its correctness"], status=status.HTTP_400_BAD_REQUEST)




class RequestView(APIView):
    def get_object(self, pk):
        # Response(["Request id must be integer!"])
        if type(pk) != int:
            return Response(["Request id must be integer!"], status=status.HTTP_400_BAD_REQUEST)#JsonResponse(["Request id must be integer!"], safe=False)
        try:
            return Request.objects.get(pk=pk)
        except Request.DoesNotExist:
            return Response(["Request does not exist!"], status=status.HTTP_400_BAD_REQUEST)


    def patch(self, request, request_id):
        request_to_update = self.get_object(request_id)
        print(type(request_to_update))
        if type(request_to_update) == Response:
            return request_to_update
        serializer = RequestSerializer(request_to_update, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, request_id):
        request_to_delete = self.get_object(request_id)
        if type(request_to_delete) == Response:
            return request_to_delete
        return Response(request_to_delete.delete(), status=status.HTTP_200_OK)



@require_http_methods(["GET"])
def get_user_requests(request, user_id):
    requests = Request.objects.filter(creator=user_id)

    if requests:
        serializer = RequestSerializer(requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(["No such user!"], status=status.HTTP_400_BAD_REQUEST)
