# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings

class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gallery',
            name='lang',
            field=models.CharField(max_length=20, verbose_name='language', choices=settings.LANGUAGES, blank=True),
        ),
    ]
