from django.db.models.signals import post_save
from django.contrib.sites.models import Site
from django.dispatch import receiver
from django.core.mail import mail_admins

from auctioneer.contact.models import ContactMessage


@receiver(post_save, sender=ContactMessage, dispatch_uid='contact.save')
def contact_save(sender, **kwargs):
    site = Site.objects.get_current()
    contact = kwargs['instance']
    subject = 'Contact message received on %s' % site.name
    msg = 'The following message was receveived at %s\n\n' % contact.created
    if contact.user is not None:
        msg += 'User ID: %s\n' % contact.user.id
    msg += 'Name: %s\n' % contact.name
    msg += 'Email: %s\n' % contact.email
    msg += 'Message: \n\n%s\n\n' % contact.message
    mail_admins(subject, msg)
