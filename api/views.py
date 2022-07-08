from django.views.decorators.http import require_http_methods
import json

from django.http import JsonResponse

from .models import User, UserRole, Role

@require_http_methods(['GET'])
def get_users(requests):
    users_with_roles = []
    for user in User.objects.all():
        service_id = user.service_id
        roles = []
        for user_role in UserRole.objects.filter(user=service_id):
            roles.append(user_role.role.name)

        users_with_roles.append({'service_id': service_id, 'roles': roles})
    return JsonResponse(users_with_roles, safe=False)


@require_http_methods(['POST'])
def add_users(request):
    users = json.loads(request.body)
    print(users)
    for user in users:
        new_user = User(service_id=user['service_id'])
        new_user.save()

        for role in user['roles']:
            new_user_role = UserRole(user=new_user, role=Role.objects.get(name=role))
            try:
                new_user_role.validate_unique()
            except:
                print("This role already exists for the current user")
            else:
                new_user_role.save()

    return JsonResponse(list(User.objects.all().values()), safe=False)
