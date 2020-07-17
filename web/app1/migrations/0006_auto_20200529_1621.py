# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2020-05-29 16:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0005_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='icon',
            field=models.ImageField(default='icons/2020/03/default.jpg', null=True, upload_to='icons/%Y/%m'),
        ),
        migrations.AlterField(
            model_name='person',
            name='mail',
            field=models.CharField(max_length=32, null=True),
        ),
    ]