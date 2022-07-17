from rest_framework import serializers
from .models import (
    Role, 
    User, 
    UserRole,
    Request,
    RequestHistory,
)
from rest_framework.validators import UniqueValidator
from .services import CustomException
from .services import get_request



class UserSerializer(serializers.Serializer):

    service_id = serializers.CharField(
        max_length=11, 
        required=True, 
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    def create(self, validated_data):
        return User.objects.create(**validated_data)



class UserRoleSerializer(serializers.Serializer):

    service_id = serializers.CharField(max_length=11, required=True)
    roles = serializers.ListField(
        child = serializers.CharField(max_length=2),
        min_length=1,
    )


    def validate_roles(self, values):
        if not values:
            raise serializers.ValidationError("roles can't be empty!")

        roles_to_print, roles = [], []
        for role in Role.objects.all():
            roles_to_print.append(role.name)
            roles.append(role.name)

        roles_to_print = ["'" + elem + "'" for elem in roles]
        
        for value in values:
            if value not in roles:
                error_message = f'role must be in [{", ".join(roles_to_print)}]'
                raise serializers.ValidationError(error_message)
        return values


    def create(self, validated_data):
        user = User.objects.get(service_id=validated_data['service_id'])

        for role in validated_data['roles']:
            user_role = UserRole(
                user=user,
                role=Role.objects.get(pk=role)
            )
            user_role.validate_unique()
            user_role.save()
                
        return validated_data



class RequestSerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)
    creator = serializers.CharField(max_length=11, required=True)
    reviewer = serializers.CharField(max_length=11, required=True)
    status = serializers.CharField(required=False)
    bonus_type = serializers.CharField(required=True)
    description = serializers.CharField(required=True)
    creation_time = serializers.DateTimeField(required=False)
    paymant_day = serializers.DateTimeField(required=False)


    def validate_creator(self, value):
        user = User.objects.filter(service_id=value).first()
        if not user:
            raise CustomException("No such user for 'creator' field!")
        return value


    def validate_reviewer(self, value):
        user = User.objects.filter(service_id=value).first()
        if not user:
            raise CustomException("No such user for 'reviewer' field!")

        if not UserRole.objects.filter(user=user, role=Role.objects.get(name='r')):
            raise CustomException("Your supposed reviewer isn't actually reviewer!")

        return value


    def validate_status(self, value):
        choices = Request.Status.values

        choices_to_print = []
        for choice in choices:
            choices_to_print.append(choice)

        choices_to_print = ["'" + elem + "'" for elem in choices_to_print]

        if value not in choices:
            message = f"'status' field must be in [{', '.join(choices_to_print)}]"
            raise CustomException(message)

        return value


    def is_creation_time_valid(self, value):
        if value:
            raise CustomException("It's forbidden to change the 'creation_time' field!")


    def create(self, validated_data):
        if 'creation_time' in validated_data:
            self.is_creation_time_valid(validated_data['creation_time'])

        if 'status' in validated_data and validated_data['status'] in ('a', 'r', 'p'):
            error_message = f"It's forbidden to set 'status' field with '{validated_data['status']}' value on request creation!"
            raise CustomException(error_message)

        data_to_save = validated_data.copy()
        data_to_save['creator'] = User.objects.get(service_id=data_to_save['creator'])
        data_to_save['reviewer'] = User.objects.get(service_id=data_to_save['reviewer'])

        request = Request.objects.create(**data_to_save)
        data_for_history_serializer = {
            'request': request,
        }

        RequestHistorySerializer(data=data_for_history_serializer).save()

        return get_request(request)


    def update(self, instance, validated_data):
        if instance.status == 'p':
            raise CustomException("This request is paid, so closed and can't be updated!")
        elif instance.status == 'r':
            raise CustomException("This request is rejected, so can't be updated and approved later!")
        elif instance.status == 'c' and validated_data['status'] == 'c':
            raise CustomException("This request is alread, so can't be recreated!")
            
        forbidden_fields = ['creator', 'creation_time']
        for field in forbidden_fields:
            if field in validated_data:
                error_message = f"'{field}' field can't be changed!"
                raise CustomException(error_message)

        if 'status' in validated_data and validated_data['status'] == 'a':
            raise CustomException("You must provide 'paymant_day' field to change status to 'approved'!")

        try:
            reviewer = User.objects.filter(pk=validated_data['reviewer']).first()
        except KeyError:
            reviewer = instance.reviewer

        instance.reviewer = reviewer
        instance.status = validated_data.get('status', 'e')
        instance.bonus_type = validated_data.get('bonus_type', instance.bonus_type)
        instance.description = validated_data.get('description', instance.description)
        instance.paymant_day = validated_data.get('paymant_day', instance.paymant_day)
        instance.save()

        data_for_history_serializer = {
            "request": instance,
            "type_of_change": instance.status,
        }
        
        RequestHistorySerializer(data=data_for_history_serializer).save()

        return get_request(instance)



class RequestHistorySerializer(serializers.Serializer):
    request = serializers.IntegerField(required=True)
    modified = serializers.DateTimeField(required=False)
    type_of_change = serializers.CharField(required=False)


    def validate_type_of_change(self, value):
        choices = RequestHistory.TypeOfChange.values

        choices_to_print = []
        for choice in choices:
            choices_to_print.append(choice)

        choices_to_print = ["'" + elem + "'" for elem in choices_to_print]

        if value not in choices:
            message = f"'type_of_change' field must be in [{', '.join(choices_to_print)}]"
            raise CustomException(message)

        return value


    def create(self, validated_data):
        request = Request.objects.get(id=validated_data['request'])    
        validated_data['request'] = request
        return RequestHistory.objects.create(**validated_data)
                    