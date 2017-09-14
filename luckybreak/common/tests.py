from unittest import skipIf
from contextlib import contextmanager

from django.urls import reverse
from django.conf import settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import staleness_of
from test_plus.test import TestCase
from rest_framework.test import APITestCase

from luckybreak.users.models import User
from luckybreak.users.tests.factories import UserFactory, GuestFactory, ProviderFactory

SKIP_TESTS = True
if hasattr(settings, 'SKIP_FUNCTIONAL_TESTS'):
    SKIP_TESTS = settings.SKIP_FUNCTIONAL_TESTS

SKIP_TEXT = 'Functional tests are disabled'


class BaseFunctionalTestCase(StaticLiveServerTestCase):
    skip_tests = SKIP_TESTS

    @skipIf(SKIP_TESTS, SKIP_TEXT)
    def setUp(self):
        super(BaseFunctionalTestCase, self).setUp()

        self.selenium = webdriver.Chrome()
        self.selenium.implicitly_wait(30)
        self.selenium.maximize_window()

        self.guest = GuestFactory(username='testguest')
        self.guest.save()
        self.provider = ProviderFactory(username='testprovider')
        self.provider.save()

    def tearDown(self):
        self.selenium.quit()

    def live_url(self, url_name):
        return '{}{}'.format(
            self.live_server_url,
            reverse(url_name)
        )

    @contextmanager
    def wait_for_page_load(self, timeout=30):
        old_page = self.selenium.find_element_by_tag_name('html')
        yield
        WebDriverWait(self.selenium, timeout).until(
            staleness_of(old_page)
        )

    def guest_login(self):
        self.selenium.get(self.live_url('account_login'))
        self.selenium.find_element_by_id('id_login').send_keys(self.guest.email)
        self.selenium.find_element_by_id('id_password').send_keys('password')
        self.selenium.find_element_by_id('signin-submit').click()

    def provider_login(self):
        self.selenium.get(self.live_url('account_login'))
        self.selenium.find_element_by_id('id_login').send_keys(self.provider.email)
        self.selenium.find_element_by_id('id_password').send_keys('password')
        self.selenium.find_element_by_id('signin-submit').click()


class BaseTestCase(TestCase):
    user_factory = UserFactory

    def setUp(self):
        self.guest = self.make_guest()
        self.provider = self.make_provider()

    def make_guest(self):
        user = self.make_user(username='testguest')
        user.user_type = User.USER_TYPE_GUEST
        user.save()
        return user

    def make_provider(self):
        user = self.make_user(username='testprovider')
        user.user_type = User.USER_TYPE_PROVIDER
        user.save()
        return user


class BaseAPITestCase(APITestCase):
    def setUp(self):
        self.guest = GuestFactory(username='testguest')
        self.guest.save()
        self.provider = ProviderFactory(username='testprovider')
        self.provider.save()
