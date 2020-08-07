# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2020-08-06 22:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0004_notice_discussion_res_res'),
    ]

    operations = [
        migrations.AddField(
            model_name='discussionresponseresponse',
            name='comment_res',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app1.DiscussionResponseResponse', verbose_name='DRR'),
        ),
        migrations.AddField(
            model_name='discussionresponseresponse',
            name='discussion',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app1.Discussion'),
        ),
        migrations.AddField(
            model_name='discussionresponseresponse',
            name='type',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='notice',
            name='discussion_R_R',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='res_res', to='app1.DiscussionResponseResponse'),
        ),
        migrations.AlterField(
            model_name='discussionresponseresponse',
            name='comment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app1.DiscussionResponse'),
        ),
        migrations.AlterField(
            model_name='notice',
            name='discussion_res_res',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='res', to='app1.DiscussionResponseResponse'),
        ),
    ]