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
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('title', models.CharField(max_length=128, blank=True)),
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
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=128, verbose_name='Name')),
                ('parent', models.ForeignKey(to='widgets.PageType', blank=True, null=True, on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name': 'Pagetype',
                'verbose_name_plural': 'Pagetypes',
            },
        ),
        migrations.CreateModel(
            name='PageTypeDescription',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('lang', models.CharField(max_length=20, blank=True, verbose_name='language', choices=settings.LANGUAGES)),
                ('description', models.CharField(max_length=156, help_text='Description (for Metatag/seo)', blank=True, verbose_name='Description')),
                ('pagetype', models.ForeignKey(to='widgets.PageType', on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name': 'Pagetype-Description',
                'verbose_name_plural': 'Pagetype-Descriptions',
            },
        ),
        migrations.CreateModel(
            name='TemplateTagWidget',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('title', models.CharField(max_length=128, blank=True)),
                ('name', models.SlugField(verbose_name='name', unique=True)),
                ('renderclasskey', models.CharField(max_length=255, choices=sorted([(w, w) for w in widget_settings.TEMPLATETAG_WIDGETS]))),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TypeArea',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('lang', models.CharField(max_length=20, blank=True, verbose_name='language', choices=settings.LANGUAGES)),
                ('area', models.CharField(max_length=64, choices=sorted([(a) for a in widget_settings.AREAS ]))),
                ('type', models.ForeignKey(to='widgets.PageType', on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name': 'Pagetype-Area',
                'verbose_name_plural': 'Pagetype-Areas',
            },
        ),
        migrations.CreateModel(
            name='WidgetInArea',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('object_id', models.PositiveIntegerField()),
                ('position', models.PositiveIntegerField()),
                ('enabled', models.BooleanField(verbose_name='enabled', default=False)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType', on_delete=models.CASCADE)),
                ('typearea', models.ForeignKey(related_name='widgets', to='widgets.TypeArea', on_delete=models.CASCADE)),
            ],
            options={
                'ordering': ['position'],
            },
        ),
        migrations.AlterUniqueTogether(
            name='typearea',
            unique_together=set([('area', 'type', 'lang')]),
        ),
        migrations.AlterUniqueTogether(
            name='pagetypedescription',
            unique_together=set([('pagetype', 'lang')]),
        ),
    ]
