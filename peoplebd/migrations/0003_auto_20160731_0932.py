# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-07-31 06:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('peoplebd', '0002_person_busy'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
            ],
        ),
        migrations.AddField(
            model_name='person',
            name='category',
            field=models.ManyToManyField(blank=True, related_name='who_do', to='peoplebd.Category'),
        ),
    ]
