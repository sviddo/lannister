from django.core.exceptions import ValidationError
from django.db import models

class User(models.Model):
    service_id = models.CharField(max_length=11, primary_key=True)

class Role(models.Model):
    class ExistingRoles(models.TextChoices):
        COMMON_WORKER = 'cw'
        REVIEWER = 'r'
        ADMINISTRATOR = 'a'

    name = models.CharField(max_length=2, choices=ExistingRoles.choices, primary_key=True)

class UserRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, default='cw')

    def validate_unique(self, exclude=None):
        if UserRole.objects.exclude(id=self.id).filter(user=self.user, \
                                 role=self.role).exists():
            raise ValidationError("Model already exists")
        super(UserRole, self).validate_unique(exclude)

