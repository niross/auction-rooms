# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-08-17 06:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='search_appearance_count',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='auction',
            name='view_count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
