# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
from pagetools.widgets import settings as widget_settings

class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContentWidget',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('title', models.CharField(blank=True, max_length=128)),
                ('name', models.SlugField(verbose_name='name', unique=True)),
                ('content', models.TextField(verbose_name='Content')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PageType',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(verbose_name='Name', max_length=128)),
                ('description', models.CharField(blank=True, help_text='Description (for Metatag/seo)', verbose_name='Description', max_length=156)),
                ('parent', models.ForeignKey(blank=True, to='widgets.PageType', null=True)),
            ],
            options={
                'verbose_name': 'Pagetype',
            },
        ),
        migrations.CreateModel(
            name='TemplateTagWidget',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('title', models.CharField(blank=True, max_length=128)),
                ('name', models.SlugField(verbose_name='name', unique=True)),
                ('renderclasskey', models.CharField(max_length=255, choices=[(w, w) for w in widget_settings.TEMPLATETAG_WIDGETS])),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TypeArea',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('lang', models.CharField(max_length=20, blank=True, verbose_name='language', choices=settings.LANGUAGES)),
                ('area', models.CharField(max_length=64, choices=[(a[0], a[0]) for a in widget_settings.AREAS ])),
                ('type', models.ForeignKey(to='widgets.PageType')),
            ],
            options={
                'verbose_name': 'Pagetype-Area',
                'verbose_name_plural': 'Pagetype-Areas',
            },
        ),
        migrations.CreateModel(
            name='WidgetInArea',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
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
