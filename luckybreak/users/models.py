from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class User(AbstractUser):
    USER_TYPE_GUEST = 1
    USER_TYPE_PROVIDER = 2
    _USER_TYPE_CHOICES = (
        (USER_TYPE_GUEST, 'Guest'),
        (USER_TYPE_PROVIDER, 'Provider'),
    )
    user_type = models.IntegerField(
        choices=_USER_TYPE_CHOICES
    )
    phone = models.CharField(
        max_length=100, null=True, blank=True
    )

    def __str__(self):
        return self.get_full_name()
