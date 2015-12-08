# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import pagetools.subscribe.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='QueuedEmail',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
            ('lang', models.CharField(max_length=20, blank=True, verbose_name='language', choices=settings.LANGUAGES)),
                ('createdate', models.DateTimeField(verbose_name='Created on', auto_now_add=True)),
                ('modifydate', models.DateTimeField(verbose_name='Last modified on', auto_now_add=True)),
                ('senddate', models.DateTimeField(verbose_name='Send after', auto_now_add=True)),
                ('subject', models.CharField(blank=True, default='', verbose_name='Subject', max_length=255)),
                ('body', models.TextField(blank=True, default='', verbose_name='Body')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'News-Mail',
            },
        ),
        migrations.CreateModel(
            name='SendStatus',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
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
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('lang', models.CharField(max_length=20, blank=True, verbose_name='language', choices=settings.LANGUAGES)),
                ('is_activated', models.BooleanField(default=False)),
                ('subscribtion_date', models.DateTimeField(auto_now_add=True)),
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
