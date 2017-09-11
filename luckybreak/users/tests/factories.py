import factory

from luckybreak.users.models import User


class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Sequence(lambda n: 'user-{0}'.format(n))
    email = factory.Sequence(lambda n: 'user-{0}@example.com'.format(n))
    password = factory.PostGenerationMethodCall('set_password', 'password')
    user_type = 1

    class Meta:
        model = 'users.User'
        django_get_or_create = ('email', )


class GuestFactory(UserFactory):
    user_type = User.USER_TYPE_GUEST


class ProviderFactory(UserFactory):
    user_type = User.USER_TYPE_PROVIDER
