from unittest import skipIf
from contextlib import contextmanager

from channels.test import ChannelTestCase
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
    fixtures = ['users.json']

    @skipIf(SKIP_TESTS, SKIP_TEXT)
    def setUp(self):
        self.selenium = webdriver.Chrome()
        self.guest = User.objects.get(pk=1)
        self.guest.set_password('password')
        self.guest.save()
        self.provider = User.objects.get(pk=2)
        self.provider.set_password('password')
        self.provider.save()
        super(BaseFunctionalTestCase, self).setUp()

    def tearDown(self):
        self.selenium.quit()

    def live_url(self, url_name, kwargs=None):
        return '{}{}'.format(
            self.live_server_url,
            reverse(url_name, kwargs=kwargs)
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
    fixtures = ['users.json']

    def setUp(self):
        self.guest = User.objects.get(pk=1)
        self.guest.set_password('password')
        self.guest.save()
        self.provider = User.objects.get(pk=2)
        self.provider.set_password('password')
        self.provider.save()

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
    fixtures = ['users.json']

    def setUp(self):
        self.guest = User.objects.get(pk=1)
        self.guest.set_password('password')
        self.guest.save()
        self.provider = User.objects.get(pk=2)
        self.provider.set_password('password')
        self.provider.save()


class BaseChannelTestCase(ChannelTestCase):
    fixtures = ['users.json']

    def setUp(self):
        self.guest = User.objects.get(pk=1)
        self.guest.set_password('password')
        self.guest.save()
        self.provider = User.objects.get(pk=2)
        self.provider.set_password('password')
        self.provider.save()
