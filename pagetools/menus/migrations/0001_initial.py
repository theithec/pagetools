# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('title', models.CharField(verbose_name='Title', max_length=128)),
                ('enabled', models.BooleanField(verbose_name='enabled', default=True)),
                ('url', models.CharField(verbose_name='URL', max_length=255)),
            ],
            options={
                'verbose_name': 'Link',
                'verbose_name_plural': 'Links',
            },
        ),
        migrations.CreateModel(
            name='MenuCache',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('cache', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='MenuEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('lang', models.CharField(choices=settings.LANGUAGES, verbose_name='language', max_length=20, blank=True)),
                ('title', models.CharField(verbose_name='Title', max_length=128)),
                ('slugs', models.CharField(verbose_name='slugs', max_length=512, help_text='Whitespace separated slugs of content', blank=True, default='')),
                ('object_id', models.PositiveIntegerField()),
                ('enabled', models.BooleanField(default=False)),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('parent', mptt.fields.TreeForeignKey(related_name='children', blank=True, to='menus.MenuEntry', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ViewLink',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('title', models.CharField(verbose_name='Title', max_length=128)),
                ('enabled', models.BooleanField(verbose_name='enabled', default=True)),
                ('name', models.CharField(verbose_name='Name', max_length=255)),
            ],
            options={
                'verbose_name': 'ViewLink',
                'verbose_name_plural': 'ViewLinks',
            },
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
            ],
            options={
                'verbose_name': 'Menu',
                'proxy': True,
            },
            bases=('menus.menuentry',),
        ),
        migrations.AlterUniqueTogether(
            name='menuentry',
            unique_together=set([('title', 'lang')]),
        ),
        migrations.AddField(
            model_name='menucache',
            name='menu',
            field=models.OneToOneField(blank=True, to='menus.Menu', null=True),
        ),
    ]
