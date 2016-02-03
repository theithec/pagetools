# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import pagetools.core.models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0003_auto_20151220_1809'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='slug',
            field=pagetools.core.models.USlugField(max_length=255, verbose_name='Slug'),
        ),
    ]
