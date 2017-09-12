from django.core import mail

from luckybreak.common.tests import BaseFunctionalTestCase


class AuthTestCase(BaseFunctionalTestCase):
    def test_send_contact_message(self):
        self.selenium.get(self.live_url('contact:contact'))
        self.selenium.find_element_by_id('id_name').send_keys('William Moreland')
        self.selenium.find_element_by_id('id_email').send_keys('bunk@baltimorepd.com')
        self.selenium.find_element_by_id('id_message').send_keys('test message')
        self.selenium.find_element_by_id('contact-submit').click()
        self.assertEqual(len(mail.outbox), 1)
