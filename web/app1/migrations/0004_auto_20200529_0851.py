# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2020-05-29 08:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0003_articlecomment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='mail',
            field=models.CharField(max_length=16, null=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='password',
            field=models.CharField(max_length=256),
        ),
    ]
