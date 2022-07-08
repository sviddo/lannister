from django.apps import AppConfig
import requests

class SlackConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'slack'

    def ready(self) -> None:
        from api.models import Role
        from .services import get_db_ready_user_list

        common_worker = Role(name='cw')
        common_worker.save()

        reviewer = Role(name='r')
        reviewer.save()

        administrator = Role(name='a')
        administrator.save()

        #users = get_db_ready_user_list()
        #requests.post('http://127.0.0.1:8000/api/add_users/', json=users)


