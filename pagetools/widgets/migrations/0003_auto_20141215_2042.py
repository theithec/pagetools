# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('widgets', '0002_auto_20141215_1941'),
    ]

    operations = [
        migrations.AlterField(
            model_name='templatetagwidget',
            name='renderclasskey',
            field=models.CharField(choices=[('recommend', 'recommend'), ('latest_events', 'latest_events'), ('latest_events_in_city', 'latest_events_in_city')], max_length=255),
            preserve_default=True,
        ),
    ]
