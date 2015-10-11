# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('widgets', '0004_auto_20151007_1615'),
    ]

    operations = [
        migrations.AlterField(
            model_name='templatetagwidget',
            name='renderclasskey',
            field=models.CharField(max_length=255, choices=[('latest_events_in_city', 'latest_events_in_city'), ('recommend', 'recommend'), ('latest_events', 'latest_events')]),
        ),
    ]
