# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import pagetools.core.models


class Migration(migrations.Migration):

    dependencies = [
        ('galleries', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gallery',
            name='slug',
            field=pagetools.core.models.USlugField(max_length=255, verbose_name='Slug'),
        ),
        migrations.AlterField(
            model_name='gallerypic',
            name='slug',
            field=pagetools.core.models.USlugField(max_length=255, verbose_name='Slug'),
        ),
    ]
