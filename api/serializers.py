from rest_framework import serializers
from .models import (
    Role, 
    User, 
    UserRole, 
)
from rest_framework.validators import UniqueValidator



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