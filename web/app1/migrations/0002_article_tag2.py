# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2020-08-04 12:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='tag2',
            field=models.CharField(blank=True, max_length=64),
        ),
    ]