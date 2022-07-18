import json
import rest_framework.serializers as ser
import django.core.exceptions as exceptions
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
from .services import CustomException
from .services import get_request



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



class ReviewerRole(APIView):
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise CustomException("User does not exist!")


    def patch(self, request, user_id):
        try:
            user_to_update = self.get_object(user_id)
        except CustomException as exc:
            exception_message = str(exc)
            return Response([exception_message], status=status.HTTP_400_BAD_REQUEST)

        if UserRole.objects.filter(user=user_to_update, role=Role.objects.get(pk='r')).first():
            return Response(["User is already reviewer!"], status=status.HTTP_400_BAD_REQUEST)

        UserRole(user=user_to_update, role=Role.objects.get(pk='r')).save()

        return Response(self.get_user(user_id), status=status.HTTP_200_OK)
        

    def delete(self, request, user_id):
        try:
            user_to_update = self.get_object(user_id)
        except CustomException as exc:
            exception_message = str(exc)
            return Response([exception_message], status=status.HTTP_400_BAD_REQUEST)

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



@api_view(["GET"])
def get_requests(request):
    requests = Request.objects.all()
    if requests:
        requests_list = []
        for elem in requests:
            temp_dict = {}
            temp_dict['id'] = elem.id
            temp_dict['creator'] = elem.creator.service_id
            temp_dict['reviewer'] = elem.reviewer.service_id
            temp_dict['status'] = elem.status
            temp_dict['bonus_type'] = elem.bonus_type
            temp_dict['description'] = elem.description
            temp_dict['creation_time'] = elem.creation_time
            temp_dict['paymant_day'] = elem.paymant_day
            requests_list.append(temp_dict)

        return Response(requests_list, status=status.HTTP_200_OK)

    return Response(["No requests created!"], status=status.HTTP_400_BAD_REQUEST)



@api_view(["POST"])
def create_request(request):
    try:
        new_request = json.loads(request.body)
    except JSONDecodeError:
        return Response(["Invalid json format! Please, check its correctness"], status=status.HTTP_400_BAD_REQUEST)
    
    serializer = RequestSerializer(data=new_request)
    try:
        if serializer.is_valid():
            pass
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
    except CustomException as exc:
        exception_message = str(exc)
        return Response([exception_message], status=status.HTTP_400_BAD_REQUEST)

    return Response(serializer.data, status=status.HTTP_201_CREATED)



class RequestView(APIView):
    def get_object(self, pk):
        try:
            int(pk)
            return Request.objects.get(pk=pk)
        except ValueError:
            raise CustomException("Request id must be integer!")
        except Request.DoesNotExist:
            raise CustomException("Request does not exist!")


    def patch(self, request, request_id):        
        try:
            request_to_update = self.get_object(request_id)
            request_data = json.loads(request.body)

            serializer = RequestSerializer(request_to_update, data=request_data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except JSONDecodeError:
            return Response(["Invalid json format! Please, check its correctness"], status=status.HTTP_400_BAD_REQUEST)

        except CustomException as exc:
            exception_message = str(exc)
            return Response([exception_message], status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, request_id):
        try:
            request_to_delete = self.get_object(request_id)
        except CustomException as exc:
            exception_message = str(exc)
            return Response([exception_message], status=status.HTTP_400_BAD_REQUEST)

        return Response(request_to_delete.delete(), status=status.HTTP_200_OK)



@api_view(["GET"])
def get_user_requests(request, user_id):
    user = User.objects.filter(service_id=user_id).first()
    if not user:
        return Response(["No such user!"], status=status.HTTP_400_BAD_REQUEST)

    requests = Request.objects.filter(creator=user_id)
    if requests:
        user_requests = []
        for elem in requests:
            user_requests.append(get_request(elem))

        return Response(user_requests, status=status.HTTP_200_OK)

    return Response(["User has no requests!"], status=status.HTTP_400_BAD_REQUEST)
