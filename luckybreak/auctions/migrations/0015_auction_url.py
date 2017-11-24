# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-24 06:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0014_auto_20171019_1752'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='url',
            field=models.URLField(blank=True, help_text='View the experience on the providers website', null=True),
        ),
    ]
