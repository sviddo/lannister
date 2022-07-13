from django.apps import AppConfig
import requests

class SlackConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'slack'

    def ready(self) -> None:
        from api.models import Role

        Role(name='cw').save()
        Role(name='r').save()
        Role(name='a').save()
