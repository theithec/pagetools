# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
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
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('title', models.CharField(verbose_name='Title', max_length=128)),
                ('enabled', models.BooleanField(default=True, verbose_name='enabled')),
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
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('cache', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='MenuEntry',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('lang', models.CharField(max_length=20, blank=True, verbose_name='language', choices=settings.LANGUAGES)),

                ('title', models.CharField(verbose_name='Title', max_length=128)),
                ('slugs', models.CharField(blank=True, default='', help_text='Whitespace separated slugs of content', verbose_name='slugs', max_length=512)),
                ('object_id', models.PositiveIntegerField()),
                ('enabled', models.BooleanField(default=False)),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('parent', mptt.fields.TreeForeignKey(blank=True, to='menus.MenuEntry', null=True, related_name='children')),
            ],
        ),
        migrations.CreateModel(
            name='ViewLink',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('title', models.CharField(verbose_name='Title', max_length=128)),
                ('enabled', models.BooleanField(default=True, verbose_name='enabled')),
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
