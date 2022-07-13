from django.http import JsonResponse
from rest_framework import serializers
from .models import Role, User, UserRole, Request
from rest_framework.validators import UniqueValidator


class UserSerializer(serializers.Serializer):
    service_id = serializers.CharField(max_length=11, required=True, validators=[UniqueValidator(queryset=User.objects.all())])

    def create(self, validated_data):
        return User.objects.create(**validated_data)



class UserRoleSerializer(serializers.Serializer):
    service_id = serializers.CharField(max_length=11, required=True)
    roles = serializers.ListField(
        child = serializers.CharField(max_length=2),
        min_length=1,
    )


    def validate_roles(self, values):
        print(values)
        if not values:
            raise serializers.ValidationError("Roles can't be empty!")

        roles_to_print, roles = [], []
        for role in Role.objects.all():
            roles_to_print.append(role.name)
            roles.append(role.name)

        roles_to_print = ["'" + elem + "'" for elem in roles]
        print(roles, roles_to_print)

        
        for value in values:
            print(value, roles)
            if value not in roles:
                message = f'Role must be in [{", ".join(roles_to_print)}]'
                raise serializers.ValidationError(message)
        print(values)
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



class RequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = Request
        fields = ["id", "creator", "reviewer", "status", "bonus_type", "description", "creation_time", "last_modification_time", "paymant_day"]