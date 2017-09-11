from test_plus.test import TestCase


class BrowseTestCase(TestCase):
    def test_homepage_get(self):
        self.get('browse:homepage')
        self.response_200()
        # TODO
        # self.assertInContext('closing_soon')

    def test_provider_marketing_get(self):
        self.get('browse:provider-marketing')
        self.response_200()
