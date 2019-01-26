# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import pagetools.subscriptions.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='QueuedEmail',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('lang', models.CharField(max_length=20, blank=True, verbose_name='language', choices=settings.LANGUAGES)),
                ('createdate', models.DateTimeField(verbose_name='Created on', auto_now_add=True)),
                ('modifydate', models.DateTimeField(verbose_name='Last modified on', auto_now_add=True)),
                ('senddate', models.DateTimeField(verbose_name='Send after', auto_now_add=True)),
                ('subject', models.CharField(max_length=255, verbose_name='Subject', default='', blank=True)),
                ('body', models.TextField(verbose_name='Body', default='', blank=True)),
            ],
            options={
                'verbose_name': 'News-Mail',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SendStatus',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('status', models.IntegerField()),
                ('queued_email', models.ForeignKey(to='subscriptions.QueuedEmail', on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name': 'Status',
                'verbose_name_plural': 'Statuses',
            },
        ),
        migrations.CreateModel(
            name='Subscriber',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('lang', models.CharField(max_length=20, blank=True, verbose_name='language', choices=settings.LANGUAGES)),
                ('is_activated', models.BooleanField(default=False)),
                ('subscribtion_date', models.DateTimeField(auto_now_add=True)),
                ('failures', models.IntegerField(default=0)),
                ('key', models.CharField(max_length=32, default=pagetools.subscriptions.models._mk_key)),
                ('email', models.EmailField(max_length=254, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='sendstatus',
            name='subscriber',
            field=models.ForeignKey(to='subscriptions.Subscriber', on_delete=models.CASCADE),
        ),
    ]
