from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class User(AbstractUser):
    phone = models.CharField(
        max_length=100, null=True, blank=True
    )

    def __str__(self):
        return self.get_full_name()
