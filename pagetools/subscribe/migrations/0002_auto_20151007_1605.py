# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subscribe', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='queuedemail',
            name='createdate',
            field=models.DateTimeField(verbose_name='Created on', auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='queuedemail',
            name='lang',
            field=models.CharField(max_length=20, verbose_name='language', choices=[('de', 'German'), ('en', 'English')], blank=True),
        ),
        migrations.AlterField(
            model_name='queuedemail',
            name='modifydate',
            field=models.DateTimeField(verbose_name='Last modified on', auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='queuedemail',
            name='senddate',
            field=models.DateTimeField(verbose_name='Send after', auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='subscriber',
            name='lang',
            field=models.CharField(max_length=20, verbose_name='language', choices=[('de', 'German'), ('en', 'English')], blank=True),
        ),
        migrations.AlterField(
            model_name='subscriber',
            name='subscribtion_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
