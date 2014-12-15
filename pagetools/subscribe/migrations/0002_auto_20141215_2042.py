# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('subscribe', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='queuedemail',
            name='createdate',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 15, 20, 42, 10, 814671, tzinfo=utc), editable=False, verbose_name='Created on', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='queuedemail',
            name='modifydate',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 15, 20, 42, 10, 814715, tzinfo=utc), editable=False, verbose_name='Last modified on', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='queuedemail',
            name='senddate',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 15, 20, 42, 10, 814741, tzinfo=utc), verbose_name='Send after', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='subscriber',
            name='subscribtion_date',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 15, 20, 42, 10, 813339, tzinfo=utc)),
            preserve_default=True,
        ),
    ]
