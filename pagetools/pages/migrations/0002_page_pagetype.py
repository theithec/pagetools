# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
        ('widgets', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='pagetype',
            field=models.ForeignKey(to='widgets.PageType', blank=True, null=True, on_delete=models.CASCADE),
        ),
    ]
