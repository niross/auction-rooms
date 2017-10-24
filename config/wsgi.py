"""
WSGI config for binday project.

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
os.environ['MAILGUN_SENDER_DOMAIN'] = 'mg.sonick.co.uk'
os.environ['DATABASE_URL'] = 'postgis://luckybreak:7?YF)zZ4dZ4pR&zM@localhost:5432/luckybreak'
os.environ['DJANGO_ADMIN_URL'] = 'admin/'


# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.
application = get_wsgi_application()

# Apply WSGI middleware here.
# from helloworld.wsgi import HelloWorldApplication
# application = HelloWorldApplication(application)
