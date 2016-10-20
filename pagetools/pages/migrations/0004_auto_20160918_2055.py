# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-09-18 20:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0003_auto_20151220_1809'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='description',
            field=models.CharField(blank=True, help_text='Description (for searchengines)', max_length=139, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='page',
            name='included_form',
            field=models.CharField(blank=True, choices=[('dummy', 'dummy')], max_length=255, verbose_name='Included form'),
        ),
        migrations.AlterField(
            model_name='page',
            name='slug',
            field=models.SlugField(allow_unicode=True, max_length=255, verbose_name='Slug'),
        ),
    ]
