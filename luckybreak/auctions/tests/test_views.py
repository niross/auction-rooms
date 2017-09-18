from luckybreak.common.tests import BaseTestCase


class ExperiencesTestCase(BaseTestCase):
    def test_unauthenticated_get(self):
        self.get('auctions:provider-auctions')
        self.response_403()

    def test_guest_get(self):
        self.client.force_login(self.guest)
        self.get('auctions:provider-auctions')
        self.response_403()

    def test_provider_get(self):
        self.client.force_login(self.provider)
        self.get('auctions:provider-auctions')
        self.response_200()
