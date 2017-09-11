from django.db import models

from luckybreak.users.models import User
from luckybreak.common.models import DeletableTimeStampedModel


class ContactMessage(DeletableTimeStampedModel):
    user = models.ForeignKey(User, null=True, blank=True)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    replied = models.BooleanField(default=False)

    def __unicode__(self):
        return 'Message from {}'.format(self.name)
