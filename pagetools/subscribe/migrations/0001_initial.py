# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import pagetools.subscribe.models
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='QueuedEmail',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('createdate', models.DateTimeField(default=datetime.datetime(2014, 12, 15, 19, 41, 45, 631507, tzinfo=utc), blank=True, verbose_name='Created on', editable=False)),
                ('modifydate', models.DateTimeField(default=datetime.datetime(2014, 12, 15, 19, 41, 45, 631550, tzinfo=utc), blank=True, verbose_name='Last modified on', editable=False)),
                ('senddate', models.DateTimeField(default=datetime.datetime(2014, 12, 15, 19, 41, 45, 631576, tzinfo=utc), blank=True, verbose_name='Send after')),
                ('subject', models.CharField(default='', blank=True, verbose_name='Subject', max_length=255)),
                ('body', models.TextField(default='', blank=True, verbose_name='Body')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'News-Mail',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SendStatus',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('status', models.IntegerField()),
                ('queued_email', models.ForeignKey(to='subscribe.QueuedEmail')),
            ],
            options={
                'verbose_name_plural': 'Statuses',
                'verbose_name': 'Status',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Subscriber',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('is_activated', models.BooleanField(default=False)),
                ('subscribtion_date', models.DateTimeField(default=datetime.datetime(2014, 12, 15, 19, 41, 45, 629886, tzinfo=utc))),
                ('failures', models.IntegerField(default=0)),
                ('key', models.CharField(default=pagetools.subscribe.models._mk_key, max_length=32)),
                ('email', models.EmailField(unique=True, max_length=75)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='sendstatus',
            name='subscriber',
            field=models.ForeignKey(to='subscribe.Subscriber'),
            preserve_default=True,
        ),
    ]
