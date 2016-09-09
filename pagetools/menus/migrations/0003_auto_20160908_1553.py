# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-09-08 15:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menus', '0002_auto_20160907_1523'),
    ]

    operations = [
        migrations.CreateModel(
            name='AutoPopulated',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128, verbose_name='Title')),
                ('enabled', models.BooleanField(default=True, verbose_name='enabled')),
                ('name', models.CharField(choices=[('a', '1')], max_length=255, verbose_name='Name')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='viewlink',
            name='name',
            field=models.CharField(choices=[('a', '1')], max_length=255, verbose_name='Name'),
        ),
    ]
