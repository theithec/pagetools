# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import pagetools.core.models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0006_auto_20161030_1520'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='slug',
            field=pagetools.core.models._USlugField(verbose_name='Slug', max_length=255),
        ),
    ]
