from django.core import mail

from luckybreak.common.tests import BaseFunctionalTestCase


class AuthTestCase(BaseFunctionalTestCase):
    def test_guest_signin(self):
        self.selenium.get(self.live_url('account_login'))
        self.selenium.find_element_by_id('id_login').send_keys(self.guest.email)
        self.selenium.find_element_by_id('id_password').send_keys('password')
        self.selenium.find_element_by_id('signin-submit').click()
        self.selenium.find_element_by_class_name('guest-dashboard')

    def test_provider_signin(self):
        self.selenium.get(self.live_url('account_login'))
        self.selenium.find_element_by_id('id_login').send_keys(self.provider.email)
        self.selenium.find_element_by_id('id_password').send_keys('password')
        self.selenium.find_element_by_id('signin-submit').click()
        self.selenium.find_element_by_class_name('provider-dashboard')

    def test_guest_forgot_password(self):
        self.selenium.get(self.live_url('account_login'))
        self.selenium.find_element_by_id('forgot-link').click()
        self.selenium.find_element_by_id('id_email').send_keys(self.guest.email)
        self.selenium.find_element_by_id('forgot-submit').click()
        self.selenium.find_element_by_class_name('password-reset-done')
        self.assertEqual(len(mail.outbox), 1)

    def test_provider_forgot_password(self):
        self.selenium.get(self.live_url('account_login'))
        self.selenium.find_element_by_id('forgot-link').click()
        self.selenium.find_element_by_id('id_email').send_keys(self.provider.email)
        self.selenium.find_element_by_id('forgot-submit').click()
        self.selenium.find_element_by_class_name('password-reset-done')
        self.assertEqual(len(mail.outbox), 1)

    def test_guest_signup(self):
        self.selenium.get(self.live_url('users:guest-signup'))
        self.selenium.find_element_by_id('id_first_name').send_keys('Felicia')
        self.selenium.find_element_by_id('id_last_name').send_keys('Pearson')
        self.selenium.find_element_by_id('id_email').send_keys('felicia@hotmail.com')
        self.selenium.find_element_by_id('id_password1').send_keys('Adsasf34')
        self.selenium.find_element_by_id('id_password2').send_keys('Adsasf34')
        self.selenium.find_element_by_id('signup-submit').click()
        self.selenium.find_element_by_class_name('guest-dashboard')
        self.assertEqual(len(mail.outbox), 1)

    def test_provider_signup(self):
        self.selenium.get(self.live_url('users:provider-signup'))
        self.selenium.find_element_by_id('id_first_name').send_keys('Omar')
        self.selenium.find_element_by_id('id_last_name').send_keys('Little')
        self.selenium.find_element_by_id('id_email').send_keys('omar@hotmail.com')
        self.selenium.find_element_by_id('id_phone').send_keys('1234567890')
        self.selenium.find_element_by_id('id_password1').send_keys('Adsasf34')
        self.selenium.find_element_by_id('id_password2').send_keys('Adsasf34')
        self.selenium.find_element_by_id('signup-submit').click()
        self.selenium.find_element_by_class_name('provider-dashboard')
        self.assertEqual(len(mail.outbox), 1)
