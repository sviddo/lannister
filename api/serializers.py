from rest_framework import serializers
from .models import (
    Role, 
    User, 
    UserRole,
    Request,
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
    status = serializers.CharField(required=True)
    bonus_type = serializers.CharField(required=True)
    description = serializers.CharField(required=True)
    creation_time = serializers.DateTimeField(required=False)
    last_modification_time = serializers.DateTimeField(required=False)
    paymant_day = serializers.DateTimeField(required=False)


    def is_creator_valid(self, value):
        user = User.objects.filter(service_id=value).first()
        if not user:
            raise CustomException("No such user for 'creator' field!")
        return value


    def is_reviewer_valid(self, value):
        user = User.objects.filter(service_id=value).first()
        if not user:
            raise CustomException("No such user for 'reviewer' field!")

        if not UserRole.objects.filter(user=user, role=Role.objects.get(name='r')):
            raise CustomException("Your supposed reviewer isn't actually reviewer!")

        return value


    def is_status_valid(self, value):
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

    
    def is_last_modification_time_valid(self, value):
        if value:
            raise CustomException("It's forbidden to change the 'last_modification_time' field!")


    def create(self, validated_data):
        fields_to_check = {
            'creator': self.is_creator_valid, 
            'reviewer': self.is_reviewer_valid, 
            'status': self.is_status_valid, 
            'creation_time': self.is_creation_time_valid, 
            'last_modification_time': self.is_last_modification_time_valid
        }
        for key, value in fields_to_check.items():
            if key in validated_data:
                value(validated_data[key])

        probably_unique_fields = {
            "creator": validated_data['creator'],
            "reviewer": validated_data['reviewer'],
            "bonus_type": validated_data['bonus_type'],
            "status": validated_data['status'],
        }

        if Request.objects.filter(**probably_unique_fields).first():
            raise CustomException("Such request already exists!")

        data_to_save = validated_data.copy()
        data_to_save['creator'] = User.objects.get(service_id=data_to_save['creator'])
        data_to_save['reviewer'] = User.objects.get(service_id=data_to_save['reviewer'])

        Request.objects.create(**data_to_save)

        return validated_data


    def update(self, instance, validated_data):
        forbidden_fields = ['creator', 'reviewer', 'creation_time', 'last_modification_time']
        for field in forbidden_fields:
            if field in validated_data:
                error_message = f"'{field}' field can\'t be changed!"
                raise CustomException(error_message)

        instance.status = validated_data.get('status', instance.status)
        instance.bonus_type = validated_data.get('bonus_type', instance.bonus_type)
        instance.description = validated_data.get('description', instance.description)
        instance.paymant_day = validated_data.get('paymant_day', instance.paymant_day)

        instance.save()

        return get_request(instance)
        