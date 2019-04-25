# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2019-04-24 07:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('studentCMS', '0005_auto_20190423_1856'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='成绩主键')),
                ('context', tinymce.models.HTMLField(verbose_name='留言内容')),
                ('pub_time', models.DateTimeField(auto_now_add=True, verbose_name='发布时间')),
                ('mod_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='studentCMS.Teacher')),
            ],
            options={
                'db_table': 't_notice',
                'ordering': ['-pub_time', 'id'],
            },
        ),
        migrations.AlterField(
            model_name='student',
            name='enter_date',
            field=models.DateTimeField(auto_now=True, verbose_name='入学时间'),
        ),
    ]
