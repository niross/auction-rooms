from django.db import models
from django.db.models.signals import post_delete, pre_delete

from django_extensions.db.models import TimeStampedModel


class DeletableTimeStampedQuerySet(models.Manager):
    def live(self):
        """
        Returns objects that have not been deleted
        :return:
        """
        return self.get_queryset().filter(deleted=False)


class DeletableTimeStampedModel(TimeStampedModel):
    deleted = models.BooleanField(default=False)
    objects = DeletableTimeStampedQuerySet()

    class Meta:
        abstract = True
        get_latest_by = 'created'

    def delete(self, **kwargs):
        force = kwargs.pop('force', False)
        if force:
            super(DeletableTimeStampedModel, self).delete(**kwargs)
        else:
            pre_delete.send(self.__class__, instance=self)
            self.deleted = True
            self.save()
            post_delete.send(self.__class__, instance=self)
