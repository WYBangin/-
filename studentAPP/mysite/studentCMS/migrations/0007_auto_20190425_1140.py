# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2019-04-25 03:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studentCMS', '0006_auto_20190424_1529'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='is_shield',
            field=models.IntegerField(default=0, verbose_name='是否屏蔽'),
        ),
        migrations.AddField(
            model_name='teacher',
            name='is_shield',
            field=models.IntegerField(default=0, verbose_name='是否屏蔽'),
        ),
    ]
