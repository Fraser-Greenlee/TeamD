# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-22 19:53
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stockedup', '0004_auto_20170321_1252'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='lastUpdated',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
