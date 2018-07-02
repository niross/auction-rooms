from django.test import TestCase
from django.core.urlresolvers import reverse
from django.core import mail

from auction_rooms.contact.models import ContactMessage


class ContactTest(TestCase):
    """
    Test creating a contact message
    """
    fixtures = ['users.json']

    def test_page_load(self):
        response = self.client.get(reverse('contact:contact'))
        self.assertEqual(response.status_code, 200)

    def test_submit(self):
        msg_count = ContactMessage.objects.all().count()
        mail_count = len(mail.outbox)
        form = {
            'name': 'Bob Boberson',
            'email': 'bob@bobersons.com',
            'message': 'test message'
        }
        response = self.client.post(reverse('contact:contact'), form, follow=True)
        self.assertRedirects(response, reverse('contact:contact'))
        self.assertEqual(msg_count+1, ContactMessage.objects.all().count())
        self.assertEquals(mail_count+1, len(mail.outbox))
