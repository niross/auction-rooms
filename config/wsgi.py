"""
WSGI config for luckbreak project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it also
might make sense to replace the whole Django WSGI application with a custom one
that later delegates to the Django one. For example, you could introduce WSGI
middleware here, or combine a Django application with an application of another
framework.

"""
import os
import sys

from django.core.wsgi import get_wsgi_application

sys.path.insert(0, os.path.join(os.path.abspath(os.path.dirname(__file__)), '../'))

# We defer to a DJANGO_SETTINGS_MODULE already in the environment. This breaks
# if running multiple sites in the same mod_wsgi process. To fix this, use
# mod_wsgi daemon mode with each site in its own daemon process, or use
# os.environ["DJANGO_SETTINGS_MODULE"] = "config.settings.production"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")


## Secret settings
os.environ['DJANGO_SECRET_KEY'] = '%qh^s8^(oz&zcti*bta77i!k0t+jk4)!2_@yqy4@b_##_z#0b3'
os.environ['DJANGO_EMAIL_BACKEND'] = 'anymail.backends.mailgun.MailgunBackend'
os.environ['DJANGO_MAILGUN_API_KEY'] = 'key-dd4c05abcd4edf43011db1bc4aecd8bf'
os.environ['MAILGUN_SENDER_DOMAIN'] = 'mg.luckybreak.sonick.co.uk'
os.environ['DATABASE_URL'] = 'postgis://luckybreak:7YFzZ4dZ4pR&zM@localhost:5432/luckybreak'
os.environ['DJANGO_ADMIN_URL'] = 'admin/'
os.environ['DJANGO_OPBEAT_ORGANIZATION_ID'] = 'a8c27beba6ef4c09aa8340432aa690ff'
os.environ['DJANGO_OPBEAT_APP_ID'] = '9a18256ec2'
os.environ['DJANGO_OPBEAT_SECRET_TOKEN'] = '1df6a84d68212cc7500ac7fbc4ceac641295e2e7'
os.environ['DJANGO_SENTRY_DSN'] = 'https://5ecd0ab0491240ca8a656da55e1af0d8:09f32809c8a446b29985c531df51bfff@sentry.io/234917'



# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.
application = get_wsgi_application()

# Apply WSGI middleware here.
# from helloworld.wsgi import HelloWorldApplication
# application = HelloWorldApplication(application)
