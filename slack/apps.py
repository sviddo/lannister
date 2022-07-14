from django.apps import AppConfig
from django.db.utils import OperationalError

class SlackConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'slack'

    def ready(self) -> None:
        from api.models import Role

        try:
            Role(name='cw').save()
            Role(name='r').save()
            Role(name='a').save()
        except OperationalError:
            pass
        
        
        return super().ready()
