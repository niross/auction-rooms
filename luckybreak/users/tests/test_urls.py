from django.core.urlresolvers import reverse

from test_plus.test import TestCase


class TestUserURLs(TestCase):
    """Test URL patterns for users app."""

    def setUp(self):
        self.user = self.make_user()

    def test_dashboard_reverse(self):
        """users:dashboard should reverse to /dashboard/."""
        self.assertEqual(reverse('users:dashboard'), '/dashboard/')

    def test_guest_signup_reverse(self):
        """users:guest-signup should reverse to /accounts/signup/guest/."""
        self.assertEqual(reverse('users:guest-signup'), '/accounts/signup/guest/')

    def test_provider_signup_reverse(self):
        """users:provider-signup should reverse to /accounts/signup/provider/."""
        self.assertEqual(reverse('users:provider-signup'), '/accounts/signup/provider/')
