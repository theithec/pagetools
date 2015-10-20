# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
from pagetools.widgets import settings as wsettings
from pagetools.widgets.models import TemplateTagWidget

class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContentWidget',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=128)),
                ('name', models.SlugField(unique=True, verbose_name='name')),
                ('content', models.TextField(verbose_name='Content')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PageType',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(verbose_name='Name', max_length=128)),
                ('parent', models.ForeignKey(blank=True, to='widgets.PageType', null=True)),
            ],
            options={
                'verbose_name': 'Pagetype',
            },
        ),
        migrations.CreateModel(
            name='TemplateTagWidget',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=128)),
                ('name', models.SlugField(unique=True, verbose_name='name')),
                ('renderclasskey', models.CharField(choices=TemplateTagWidget.key_choices, max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TypeArea',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('lang', models.CharField(blank=True, verbose_name='language', max_length=20, choices=settings.LANGUAGES)),
                ('area', models.CharField(max_length=64, choices=wsettings.AREAS)),
                ('type', models.ForeignKey(to='widgets.PageType')),
            ],
            options={
                'verbose_name_plural': 'Pagetype-Areas',
                'verbose_name': 'Pagetype-Area',
            },
        ),
        migrations.CreateModel(
            name='WidgetInArea',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('position', models.PositiveIntegerField()),
                ('enabled', models.BooleanField(default=False, verbose_name='enabled')),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('typearea', models.ForeignKey(related_name='widgets', to='widgets.TypeArea')),
            ],
            options={
                'ordering': ['position'],
            },
        ),
        migrations.AlterUniqueTogether(
            name='typearea',
            unique_together=set([('area', 'type', 'lang')]),
        ),
    ]
