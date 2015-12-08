# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0003_auto_20151010_1700'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='description',
            field=models.CharField(blank=True, verbose_name='Description', help_text='Description (for Metatag/seo)', max_length=156),
        ),
    ]
