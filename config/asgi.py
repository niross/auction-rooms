import os
import sys
from channels.asgi import get_channel_layer

sys.path.insert(0, os.path.join(os.path.abspath(os.path.dirname(__file__)), '../'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')
os.environ['DJANGO_SECRET_KEY'] = '%qh^s8^(oz&zcti*bta77i!k0t+jk4)!2_@yqy4@b_##_z#0b3'
os.environ['DJANGO_EMAIL_BACKEND'] = 'anymail.backends.mailgun.MailgunBackend'
os.environ['DJANGO_MAILGUN_API_KEY'] = 'key-dd4c05abcd4edf43011db1bc4aecd8bf'
os.environ['MAILGUN_SENDER_DOMAIN'] = 'mg.auction-rooms.sonick.co.uk'
os.environ['DATABASE_URL'] = 'postgis://auction-rooms:7YFzZ4dZ4pR&zM@localhost:5432/auction-rooms'
os.environ['DJANGO_ADMIN_URL'] = 'admin/'
os.environ['DJANGO_OPBEAT_ORGANIZATION_ID'] = 'a8c27beba6ef4c09aa8340432aa690ff'
os.environ['DJANGO_OPBEAT_APP_ID'] = '9a18256ec2'
os.environ['DJANGO_OPBEAT_SECRET_TOKEN'] = '1df6a84d68212cc7500ac7fbc4ceac641295e2e7'
os.environ['DJANGO_SENTRY_DSN'] = 'https://5ecd0ab0491240ca8a656da55e1af0d8:09f32809c8a446b29985c531df51bfff@sentry.io/234917'


channel_layer = get_channel_layer()
