import uuid

from django.core.management.base import BaseCommand

from auction_rooms.users.models import User


class Command(BaseCommand):
    help = "Update non-staff user emails so we don't spam them while developing"

    def handle(self, *args, **kwargs):
        update_count = 0
        for user in User.objects.filter(is_staff=False, is_superuser=False):
            user.email = str(uuid.uuid1().hex)[:14] + '@example.com'
            user.save()
            update_count += 1
        print 'Updated {} users.'.format(update_count)
