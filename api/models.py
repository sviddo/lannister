from django.core.exceptions import ValidationError
from django.db import models


class User(models.Model):
    service_id = models.CharField(max_length=11, primary_key=True)


class Role(models.Model):
    class ExistingRoles(models.TextChoices):
        COMMON_WORKER = 'cw'
        REVIEWER = 'r'
        ADMINISTRATOR = 'a'

    name = models.CharField(max_length=2, choices=ExistingRoles.choices,
                            primary_key=True)


class UserRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, default='cw')

    def validate_unique(self, exclude=None):
        if (UserRole.objects.exclude(id=self.id).
                filter(user=self.user, role=self.role).exists()):
            raise ValidationError("Model already exists")
        super().validate_unique(exclude)


class Request(models.Model):
    class Status(models.TextChoices):
        CREATED = 'c'
        APPROVED = 'a'
        REJECTED = 'r'
        PAID = 'p'

    creator = models.ForeignKey(User, on_delete=models.CASCADE,
                                related_name='created_requests')
    reviewer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                                 related_name='assigned_requests')

    # ask the user to describe the bonus type in a few words
    # i.e. - referral bonus, overtime, etc
    status = models.CharField(
        max_length=1, 
        choices=Status.choices, 
        default='c'
    )
    creation_time = models.DateTimeField(auto_now_add=True)
    paymant_day = models.DateField(null=True)
    bonus_type = models.CharField(max_length=80)
    description = models.TextField()
    

class RequestHistory(models.Model):
    class TypeOfChange(models.TextChoices):
        CREATED = 'c'
        APPROVED = 'a'
        REJECTED = 'r'
        PAID = 'p'
        EDITED = 'e'

    request = models.ForeignKey(Request, on_delete=models.CASCADE)
    modified = models.DateTimeField(auto_now_add=True)
    type_of_change = models.CharField(
        max_length=1, 
        choices=TypeOfChange.choices, 
        default='c'
    )
    
