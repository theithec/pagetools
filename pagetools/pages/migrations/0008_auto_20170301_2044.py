# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2017-03-01 20:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0007_auto_20161201_1704'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='description',
            field=models.CharField(
                blank=True,
                help_text='Description (for searchengines)',
                max_length=156,
                verbose_name='Description'),
        ),
    ]
