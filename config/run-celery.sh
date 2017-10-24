#!/bin/bash
export PYTHONPATH="/var/www/sites/luckybreak/"
export DJANGO_SETTINGS_MODULE="config.settings.production"
export DATABASE_URL="postgis://binday:zDXjS8H62DWM5Df@localhost/binday"
export FROM_EMAIL="noreply@getbindays.com"
export AWS_ACCESS_KEY_ID=""
export AWS_SECRET_ACCESS_KEY=""
export DJANGO_SECRET_KEY='db2v2at)tmxu5*wo0ww!flv+h7gn4fwoc%_y8v8*8%g7z$q19y'
export DJANGO_MAILGUN_API_KEY=key-dd4c05abcd4edf43011db1bc4aecd8bf
export MAILGUN_SENDER_DOMAIN=mg.getbindays.com
#export MAILGUN_SENDER_DOMAIN=sandbox33a74bf90740442294c91514d1726428.mailgun.org
export DJANGO_ADMIN_URL='admin/'

/home/nick/.virtualenvs/binday/bin/celery --workdir=/var/www/sites/valaduchi/bindays/binday -A binday.taskapp worker -B -s /var/log/valaduchi/binday-celerybeat-schedule -l INFO --concurrency=1

