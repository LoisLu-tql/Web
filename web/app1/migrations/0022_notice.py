# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2020-07-13 21:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0021_discussionresponse_likes_num'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('receiver_id', models.IntegerField()),
                ('sender_id', models.IntegerField()),
                ('message_type', models.IntegerField()),
                ('article_id', models.IntegerField()),
                ('article_comment_id', models.IntegerField()),
                ('discussion_id', models.IntegerField()),
                ('discussion_response_id', models.IntegerField()),
            ],
        ),
    ]
