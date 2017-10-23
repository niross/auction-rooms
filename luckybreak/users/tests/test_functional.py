import time

from django.core import mail

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from luckybreak.common.tests import BaseFunctionalTestCase
from luckybreak.users.models import User


class AuthTestCase(BaseFunctionalTestCase):
    fixtures = ['users.json']

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


class SettingsTestCase(BaseFunctionalTestCase):
    fixtures = ['users.json']

    def test_edit_settings(self):
        self.provider_login()
        self.selenium.get(self.live_url('users:settings'))
        self.selenium.find_element_by_id('id_first_name').clear()
        self.selenium.find_element_by_id('id_first_name').send_keys('Proposition Joe')
        self.selenium.find_element_by_id('id_last_name').clear()
        self.selenium.find_element_by_id('id_last_name').send_keys('Stewart')
        self.selenium.find_element_by_id('id_email').clear()
        self.selenium.find_element_by_id('id_email').send_keys('propjoe@hotmail.com')
        self.selenium.find_element_by_id('id_phone').clear()
        self.selenium.find_element_by_id('id_phone').send_keys('0987654321')
        self.selenium.find_element_by_id('settings-submit').click()

        user = User.objects.get(pk=self.provider.id)
        self.assertEqual(user.first_name, 'Proposition Joe')
        self.assertEqual(user.last_name, 'Stewart')
        self.assertEqual(user.email, 'propjoe@hotmail.com')
        self.assertEqual(user.phone, '0987654321')

    def test_change_password(self):
        self.provider_login()
        self.selenium.get(self.live_url('account_change_password'))
        self.selenium.find_element_by_id('id_oldpassword').send_keys('password')
        self.selenium.find_element_by_id('id_password1').send_keys('newpassword')
        self.selenium.find_element_by_id('id_password2').send_keys('newpassword')
        self.selenium.find_element_by_id('change-password-submit').click()
        self.selenium.execute_script('$(".logout-link").click()')

        self.selenium.get(self.live_url('account_login'))
        self.selenium.find_element_by_id('id_login').send_keys(self.provider.email)
        self.selenium.find_element_by_id('id_password').send_keys('newpassword')
        self.selenium.find_element_by_id('signin-submit').click()
        self.selenium.find_element_by_class_name('provider-dashboard')
