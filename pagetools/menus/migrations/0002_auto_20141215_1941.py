# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menus', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menuentry',
            name='lang',
            field=models.CharField(choices=[('de', 'Deutsch'), ('en', 'Englisch')], blank=True, verbose_name='language', max_length=2),
            preserve_default=True,
        ),
    ]
