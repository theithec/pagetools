# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
        ('widgets', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='pagetype',
            field=models.ForeignKey(null=True, to='widgets.PageType', blank=True),
            preserve_default=True,
        ),
    ]
