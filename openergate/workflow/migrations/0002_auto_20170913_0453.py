# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-13 04:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='work_order',
            name='update_time',
            field=models.DateTimeField(auto_now=True, verbose_name='更新时间'),
        ),
        migrations.AlterField(
            model_name='work_order',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='创建时间'),
        ),
        migrations.AlterField(
            model_name='work_order',
            name='is_active',
            field=models.IntegerField(default=1, verbose_name='是否启用'),
        ),
    ]
