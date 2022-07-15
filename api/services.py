from .models import Request
from .models import UserRole, Request


class CustomException(Exception):
    """
    this class serves as own exception class with custom messages
    """


def get_user(request: Request):
    service_id = request.service_id
    roles = []
    for user_role in UserRole.objects.filter(user=service_id):
        roles.append(user_role.role.name)

    return {'service_id': service_id, 'roles': roles}



def get_request(request: Request):
    request_data = {}

    request_data['id'] = request.id
    request_data['creator'] = request.creator.service_id
    request_data['reviewer'] = request.reviewer.service_id
    request_data['status'] = request.status
    request_data['bonus_type'] = request.bonus_type
    request_data['description'] = request.description
    request_data['creation_time'] = request.creation_time
    request_data['last_modification_time'] = request.last_modification_time
    request_data['paymant_day'] = request.paymant_day

    return request_data
