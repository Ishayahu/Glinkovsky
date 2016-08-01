# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-01 11:10
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('peoplebd', '0005_auto_20160801_1300'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='tel',
            field=models.CharField(max_length=10, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '9051112233'. Only 10 digits allowed.", regex='^\\d{10}$')]),
        ),
    ]