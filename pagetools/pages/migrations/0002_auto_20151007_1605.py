# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='lang',
            field=models.CharField(max_length=20, verbose_name='language', choices=[('de', 'German'), ('en', 'English')], blank=True),
        ),
    ]
