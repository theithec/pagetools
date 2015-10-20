# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0002_auto_20151007_1605'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pagedynformfield',
            name='name',
            field=models.CharField(verbose_name='Value', max_length=512),
        ),
    ]
