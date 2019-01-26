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
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('title', models.CharField(max_length=128, verbose_name='Title')),
                ('enabled', models.BooleanField(verbose_name='enabled', default=True)),
                ('url', models.CharField(max_length=255, verbose_name='URL')),
            ],
            options={
                'verbose_name': 'Link',
                'verbose_name_plural': 'Links',
            },
        ),
        migrations.CreateModel(
            name='MenuCache',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('cache', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='MenuEntry',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('lang', models.CharField(max_length=20, blank=True, verbose_name='language', choices=settings.LANGUAGES)),
                ('title', models.CharField(max_length=128, verbose_name='Title')),
                ('slugs', models.CharField(max_length=512, help_text='Whitespace separated slugs of content', default='', blank=True, verbose_name='slugs')),
                ('object_id', models.PositiveIntegerField()),
                ('enabled', models.BooleanField(default=False)),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType', on_delete=models.CASCADE)),
                ('parent', mptt.fields.TreeForeignKey(to='menus.MenuEntry', blank=True, related_name='children', null=True, on_delete=models.CASCADE)),
            ],
        ),
        migrations.CreateModel(
            name='ViewLink',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('title', models.CharField(max_length=128, verbose_name='Title')),
                ('enabled', models.BooleanField(verbose_name='enabled', default=True)),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
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
                'proxy': True,
                'verbose_name': 'Menu',
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
            field=models.OneToOneField(to='menus.Menu', blank=True, null=True, on_delete=models.CASCADE),
        ),
    ]
