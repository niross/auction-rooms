from django.urls import reverse
from test_plus.test import TestCase


class BrowseTestCase(TestCase):
    fixtures = [
        'currencies.json', 'users.json', 'experiences.json', 'auctions.json'
    ]

    def test_homepage_get(self):
        self.get_check_200('browse:homepage')

    def test_provider_marketing_get(self):
        self.get_check_200('browse:provider-marketing')

    def test_search(self):
        self.get_check_200('browse:search-results')
