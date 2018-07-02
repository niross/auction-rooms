from auction_rooms.common.tests import BaseTestCase
from auction_rooms.users.models import User


class UserAuthTestCase(BaseTestCase):
    def test_guest_signup_get(self):
        self.get('users:guest-signup')
        self.response_200()

    def test_guest_signup_post(self):
        self.post(
            'users:guest-signup',
            data={
                'first_name': 'Randy',
                'last_name': 'Marsh',
                'email': 'randy.marsh@iamlorde.com',
                'password1': 'correct horse battery staple',
                'password2': 'correct horse battery staple',
                'user_type': 1,
            },
        )
        self.response_302()
        self.assertEqual(
            User.objects.filter(email='randy.marsh@iamlorde.com').count(),
            1
        )


    def test_provider_signup_get(self):
        self.get('users:provider-signup')
        self.response_200()

    def test_provider_signup_post(self):
        self.post(
            'users:guest-signup',
            data={
                'first_name': 'Jimmy',
                'last_name': 'McNulty',
                'email': 'jimmy.mcnulty@baltimorepd.com',
                'password1': 'correct horse battery staple',
                'password2': 'correct horse battery staple',
                'user_type': 2,
            },
        )
        self.response_302()
        self.assertEqual(
            User.objects.filter(email='jimmy.mcnulty@baltimorepd.com').count(),
            1
        )

    def test_default_allauth_signup_get(self):
        """
        Default allauth signup page should 404
        """
        self.get('account_signup')
        self.response_404()

    def test_signin_get(self):
        self.get('account_login')
        self.response_200()

    def test_guest_signin_post(self):
        self.post(
            'account_login',
            data={
                'login': self.guest.email,
                'password': 'password',
            },
        )
        self.response_302()

    def test_provider_signin_post(self):
        self.post(
            'account_login',
            data={
                'login': self.provider.email,
                'password': 'password',
            },
        )
        self.response_302()


class DashboardTestCase(BaseTestCase):
    def test_unauthenticated_get(self):
        self.assertLoginRequired('users:dashboard')

    def test_guest_get(self):
        with self.login(username=self.guest.username, password='password'):
            self.get('users:dashboard')
            self.response_200()

    def test_provider_get(self):
        with self.login(username=self.provider.username, password='password'):
            self.get('users:dashboard')
            self.response_200()
