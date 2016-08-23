# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-08-21 20:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('peoplebd', '0010_auto_20160809_1926'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='mail',
        ),
        migrations.AddField(
            model_name='person',
            name='confirmed',
            field=models.BooleanField(default=False),
        ),
    ]