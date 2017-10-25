#!/bin/bash
export PYTHONPATH="/var/www/sites/luckybreak/"
export DJANGO_SETTINGS_MODULE="config.settings.production"
export DATABASE_URL="postgis://luckybreak:7YFzZ4dZ4pR&zM@localhost:5432/luckybreak"
export DJANGO_EMAIL_BACKEND='anymail.backends.mailgun.MailgunBackend'
export FROM_EMAIL="noreply@luckybreak.sonick.co.uk"
export AWS_ACCESS_KEY_ID=""
export AWS_SECRET_ACCESS_KEY=""
export DJANGO_SECRET_KEY='%qh^s8^(oz&zcti*bta77i!k0t+jk4)!2_@yqy4@b_##_z#0b3'
export DJANGO_MAILGUN_API_KEY=key-dd4c05abcd4edf43011db1bc4aecd8bf
export MAILGUN_SENDER_DOMAIN=mg.sonick.co.uk
export DJANGO_ADMIN_URL='admin/'
export DJANGO_OPBEAT_ORGANIZATION_ID= 'a8c27beba6ef4c09aa8340432aa690ff'
export DJANGO_OPBEAT_APP_ID='9a18256ec2'
export DJANGO_OPBEAT_SECRET_TOKEN='1df6a84d68212cc7500ac7fbc4ceac641295e2e7'
export DJANGO_SENTRY_DSN='https://5ecd0ab0491240ca8a656da55e1af0d8:09f32809c8a446b29985c531df51bfff@sentry.io/234917'

/home/nick/.virtualenvs/luckybreak/bin/celery --workdir=/var/www/sites/luckybreak -A luckybreak.taskapp worker -B -s /var/log/luckybreak/luckybreak-celerybeat-schedule -l INFO --concurrency=1

