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
            field=models.CharField(choices=[('latest_events', 'latest_events'), ('latest_events_in_city', 'latest_events_in_city'), ('recommend', 'recommend')], max_length=255),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='typearea',
            name='area',
            field=models.CharField(choices=[('sidebar', 'Sidebar'), ('header', 'Header')], max_length=64),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='typearea',
            name='lang',
            field=models.CharField(choices=[('de', 'Deutsch'), ('en', 'Englisch')], blank=True, verbose_name='language', max_length=2),
            preserve_default=True,
        ),
    ]
