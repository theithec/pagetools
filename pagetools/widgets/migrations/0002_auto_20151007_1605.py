# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('widgets', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='templatetagwidget',
            name='renderclasskey',
            field=models.CharField(max_length=255, choices=[('latest_events_in_city', 'latest_events_in_city'), ('latest_events', 'latest_events'), ('recommend', 'recommend')]),
        ),
        migrations.AlterField(
            model_name='typearea',
            name='area',
            field=models.CharField(max_length=64, choices=[('sidebar', 'Sidebar'), ('header', 'Header')]),
        ),
        migrations.AlterField(
            model_name='typearea',
            name='lang',
            field=models.CharField(max_length=20, verbose_name='language', choices=[('de', 'German'), ('en', 'English')], blank=True),
        ),
    ]
