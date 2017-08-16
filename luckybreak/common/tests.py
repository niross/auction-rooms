from unittest import skipIf

from django.conf import settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import LiveServerTestCase
from selenium import webdriver

SKIP_TESTS = True
if hasattr(settings, 'SKIP_FUNCTIONAL_TESTS'):
    SKIP_TESTS = settings.SKIP_FUNCTIONAL_TESTS

SKIP_TEXT = 'Functional tests are disabled'


class FunctionalTestCase(StaticLiveServerTestCase):
    skip_tests = SKIP_TESTS

    @skipIf(SKIP_TESTS, SKIP_TEXT)
    def setUp(self):
        self.selenium = webdriver.Chrome()
        self.selenium.implicitly_wait(30)

        self.selenium.maximize_window()
        super(FunctionalTestCase, self).setUp()

    def tearDown(self):
        # self.selenium.quit()
        super(FunctionalTestCase, self).tearDown()

    def _live_url(self, path):
        return '{}{}'.format(
            self.live_server_url,
            path
        )
