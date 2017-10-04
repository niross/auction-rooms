"""
Local settings

- Run in Debug mode

- Use mailhog for emails

- Add Django Debug Toolbar
- Add django-extensions as app
"""

from .base import *  # noqa

# DEBUG
# ------------------------------------------------------------------------------
DEBUG = env.bool('DJANGO_DEBUG', default=True)
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

# SECRET CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Note: This key only used for development and testing.
SECRET_KEY = env('DJANGO_SECRET_KEY', default='/gIF)O_1=62DB%%6%#W&u0e)]dP+5q]([IB~NnBy&w%y`QVWF^')

# Mail settings
# ------------------------------------------------------------------------------

EMAIL_PORT = 1025

EMAIL_HOST = env('EMAIL_HOST', default='mailhog')


# CACHING
# ------------------------------------------------------------------------------
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': ''
    }
}

# django-debug-toolbar
# ------------------------------------------------------------------------------
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware', ]
INSTALLED_APPS += ['debug_toolbar', ]

INTERNAL_IPS = ['127.0.0.1', '10.0.2.2', ]


import socket
import os
# tricks to have debug toolbar when developing with docker
if os.environ.get('USE_DOCKER') == 'yes':
    ip = socket.gethostbyname(socket.gethostname())
    INTERNAL_IPS += [ip[:-1] + '1']

DEBUG_TOOLBAR_CONFIG = {
    'DISABLE_PANELS': [
        'debug_toolbar.panels.redirects.RedirectsPanel',
    ],
    'SHOW_TEMPLATE_CONTEXT': True,
}

# django-extensions
# ------------------------------------------------------------------------------
INSTALLED_APPS += ['django_extensions', ]

# TESTING
# ------------------------------------------------------------------------------
TEST_RUNNER = 'django.test.runner.DiscoverRunner'

########## CELERY
# In development, all tasks will be executed locally by blocking until the task returns
CELERY_ALWAYS_EAGER = True
########## END CELERY

########## WEBPACK
# See: https://github.com/owais/django-webpack-loader
WEBPACK_LOADER = {
    'DEFAULT': {
        'CACHE': not DEBUG,
        'BUNDLE_DIR_NAME': 'js/apps/dist/js/',
        'STATS_FILE': str(
            str(APPS_DIR('static', 'js', 'apps', 'webpack-stats-dev.json'))
        ),
        'POLL_INTERVAL': 0.1,
        'TIMEOUT': None,
        'IGNORE': [r'.+\.hot-update.js', r'.+\.map']
    }
}
########## END WEBPACK

# ------------------------------------------------------------------------------

PROTOCOL = 'http://'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'asgi_redis.RedisChannelLayer',
        'ROUTING': 'luckybreak.auctions.routing.channel_routing',
        'CONFIG': {
            'hosts': [(
                'redis://:SFuScuCzTrKEKkH7d8nN9feqQ6A6HtsCf2CBT2'
                'Qc7PnDGf3zLKmav3GpvzrAEzbwcCxzFrXPzeCxBB2q@redis:6379/0'
            )]
        }
    }
}
