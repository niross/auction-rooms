# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from django.core.management import call_command


def load_fixture(apps, schema_editor):
    call_command('loaddata', 'initial_data', app_label='currencies')


def unload_fixture(apps, schema_editor):
    model = apps.get_model('currencies', 'Currency')
    model.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ('currencies', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_fixture, reverse_code=unload_fixture),
    ]
