# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2020-06-10 09:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0008_discussion'),
    ]

    operations = [
        migrations.AddField(
            model_name='discussion',
            name='add_time',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
