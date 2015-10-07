# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('subscribe', '0002_auto_20150912_1451'),
    ]

    operations = [
        migrations.AlterField(
            model_name='queuedemail',
            name='createdate',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Created on'),
        ),
        migrations.AlterField(
            model_name='queuedemail',
            name='modifydate',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Last modified on'),
        ),
        migrations.AlterField(
            model_name='queuedemail',
            name='senddate',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Send after'),
        ),
        migrations.AlterField(
            model_name='subscriber',
            name='subscribtion_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 7, 15, 38, 20, 612670, tzinfo=utc)),
        ),
    ]
