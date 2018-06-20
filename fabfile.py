import os

from datetime import datetime
from fabric.api import runs_once, lcd, local, task
from fabric.context_managers import cd, shell_env
from fabric.operations import run, sudo, get
from fabric.state import env

USER = os.environ['USER']
SITE_ROOT = '/var/www/sites/auction-rooms'
DJANGO_MANAGE = os.path.join(SITE_ROOT, 'manage.py')
VENV_ACTIVATE = '/home/nick/.virtualenvs/auction-rooms/bin/activate'
DB_PATH = os.path.join(SITE_ROOT, 'db/lander.sqlite3')

env.hosts = 'stringer'
env.port = 1004

DJANGO_ENV = {
    'DJANGO_SECRET_KEY': 'XXX',
    'DJANGO_AWS_ACCESS_KEY_ID': 'xxx',
    'DJANGO_AWS_SECRET_ACCESS_KEY': 'xxx',
    'DJANGO_MAILGUN_API_KEY': 'xxx',
    'DJANGO_ADMIN_URL': 'xxx',
    'MAILGUN_SENDER_DOMAIN': 'xxx',
    'DATABASE_URL': 'postgis://auction-rooms:7YFzZ4dZ4pR@localhost/auction-rooms'
}


def virtualenv(command):
    run('source {} && {}'.format(VENV_ACTIVATE, command))


@task
@runs_once
def register_deployment(git_path):
    with(lcd(git_path)):
        revision = local('git log -n 1 --pretty="format:%H"', capture=True)
        branch = local('git rev-parse --abbrev-ref HEAD', capture=True)
        local(
            'curl https://intake.opbeat.com/api/v1/organizations'
            '/a8c27beba6ef4c09aa8340432aa690ff/apps/9a18256ec2/releases/'
            ' -H "Authorization: Bearer '
            '1df6a84d68212cc7500ac7fbc4ceac641295e2e7"'
            ' -d rev="{}"'
            ' -d branch="{}"'
            ' -d status=completed'.format(revision, branch))


@task
def deploy():
    with(cd(SITE_ROOT)):
        with shell_env(**DJANGO_ENV):
            run('git reset --hard')
            run('git checkout master')
            run('git pull origin master')
            virtualenv('pip install -r requirements/production.txt')
            virtualenv(
                'python manage.py migrate --settings config.settings.production'
            )
            virtualenv(
                'python manage.py collectstatic --noinput '
                '--settings config.settings.production'
            )
            sudo('service apache2 reload')
            sudo('supervisorctl restart ar_celery')
            sudo('supervisorctl restart ar_asgi_daphne')
            sudo('supervisorctl restart ar_asgi_workers:*')

    register_deployment(os.path.dirname(os.path.realpath(__file__)))


@task
def import_prod_db():
    """
    Get a copy of the production database and import it locally
    """
    now = datetime.now().strftime('%Y-%m-%d')
    filename = 'auction-rooms-prod-db-backup-{}'.format(now)
    sqlpath = os.path.join('/tmp', '{}.sql'.format(filename))
    tarpath = os.path.join('/tmp', '{}.tgz'.format(filename))
    backup_dir = os.path.join(os.path.dirname(__file__), 'db-backups')

    local_tar = os.path.join(backup_dir, filename + '.tgz')
    local_sql = os.path.join(backup_dir, filename + '.sql')

    run('pg_dump -U auction-rooms auction-rooms > {}'.format(sqlpath))
    run('tar -czvf {} -C /tmp {}'.format(tarpath, '{}.sql'.format(filename)))
    get(tarpath, local_path=local_tar)
    run('rm {} {}'.format(sqlpath, tarpath))

    local('tar -xzf {} -C {}'.format(local_tar, backup_dir))
    local('docker-compose -f /home/nick/projects/auction-rooms/local.yml stop')
    local('docker-compose -f /home/nick/projects/auction-rooms/local.yml up -d postgres')
    local('psql -p 5432 -h 127.0.0.1 -U postgres -c \'drop database auction-rooms\'')
    local('psql -p 5432 -h 127.0.0.1 -U postgres -c \'create database auction-rooms\'')
    local('psql -p 5432 -h 127.0.0.1 -U postgres -d auction-rooms < {}'.format(local_sql))
    local('rm {}'.format(local_sql))
    local('docker-compose -f /home/nick/projects/auction-rooms/local.yml up -d')
    local('python /home/nick/projects/auction-rooms/manage.py scramble_user_emails')
