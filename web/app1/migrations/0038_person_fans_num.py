# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2020-07-23 19:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0037_auto_20200723_1908'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='fans_num',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
