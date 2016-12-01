# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import pagetools.core.models


class Migration(migrations.Migration):

    dependencies = [
        ('sections', '0004_auto_20160918_2055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pagenode',
            name='slug',
            field=pagetools.core.models._USlugField(verbose_name='Slug', max_length=255),
        ),
    ]
