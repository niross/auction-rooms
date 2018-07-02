from django.db.models.signals import post_save
from django.dispatch import receiver

from auction_rooms.event_log.models import EventLog
from auction_rooms.experiences.models import Experience


@receiver(post_save, sender=Experience)
def experience_save(sender, instance, created, **kwargs):
    """
    Experience post save signal handler
    :param sender:
    :param instance:
    :param created:
    :param kwargs:
    :return:
    """
    if created:
        EventLog.objects.log_experience_created(instance)
