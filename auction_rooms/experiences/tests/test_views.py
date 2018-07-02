from auction_rooms.common.tests import BaseTestCase


class ExperiencesTestCase(BaseTestCase):
    def test_unauthenticated_get(self):
        self.get('experiences:experiences')
        self.response_403()

    def test_guest_get(self):
        self.client.force_login(self.guest)
        self.get('experiences:experiences')
        self.response_403()

    def test_provider_get(self):
        self.client.force_login(self.provider)
        self.get('experiences:experiences')
        self.response_200()
