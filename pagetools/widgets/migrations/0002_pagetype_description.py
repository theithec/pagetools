# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('widgets', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pagetype',
            name='description',
            field=models.CharField(blank=True, verbose_name='Description', help_text='Description (for Metatag/seo)', max_length=156),
        ),
    ]
