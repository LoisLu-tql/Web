# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2020-07-30 13:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0041_auto_20200730_1019'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatcontent',
            name='have_read',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
