# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2020-07-24 19:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0039_discussion_last_comment_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='fans_num',
            field=models.IntegerField(default=0),
        ),
    ]
