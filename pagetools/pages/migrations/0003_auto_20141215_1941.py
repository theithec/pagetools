# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0002_page_pagetype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='lang',
            field=models.CharField(choices=[('de', 'Deutsch'), ('en', 'Englisch')], blank=True, verbose_name='language', max_length=2),
            preserve_default=True,
        ),
    ]
