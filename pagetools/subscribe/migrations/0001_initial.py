# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import pagetools.subscribe.models
from django.utils.timezone import utc
from django.conf import settings
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='QueuedEmail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('lang', models.CharField(choices=settings.LANGUAGES, max_length=20, verbose_name='language', blank=True)),
                ('createdate', models.DateTimeField(default=datetime.datetime(2015, 9, 9, 17, 51, 36, 230019, tzinfo=utc), verbose_name='Created on', blank=True, editable=False)),
                ('modifydate', models.DateTimeField(default=datetime.datetime(2015, 9, 9, 17, 51, 36, 230053, tzinfo=utc), verbose_name='Last modified on', blank=True, editable=False)),
                ('senddate', models.DateTimeField(default=datetime.datetime(2015, 9, 9, 17, 51, 36, 230078, tzinfo=utc), verbose_name='Send after', blank=True)),
                ('subject', models.CharField(default='', max_length=255, verbose_name='Subject', blank=True)),
                ('body', models.TextField(default='', verbose_name='Body', blank=True)),
            ],
            options={
                'abstract': False,
                'verbose_name': 'News-Mail',
            },
        ),
        migrations.CreateModel(
            name='SendStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.IntegerField()),
                ('queued_email', models.ForeignKey(to='subscribe.QueuedEmail')),
            ],
            options={
                'verbose_name': 'Status',
                'verbose_name_plural': 'Statuses',
            },
        ),
        migrations.CreateModel(
            name='Subscriber',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('lang', models.CharField(choices=settings.LANGUAGES, max_length=20, verbose_name='language', blank=True)),
                ('is_activated', models.BooleanField(default=False)),
                ('subscribtion_date', models.DateTimeField(default=datetime.datetime(2015, 9, 9, 17, 51, 36, 228917, tzinfo=utc))),
                ('failures', models.IntegerField(default=0)),
                ('key', models.CharField(default=pagetools.subscribe.models._mk_key, max_length=32)),
                ('email', models.EmailField(unique=True, max_length=254)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='sendstatus',
            name='subscriber',
            field=models.ForeignKey(to='subscribe.Subscriber'),
        ),
    ]
