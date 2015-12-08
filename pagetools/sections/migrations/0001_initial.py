# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import model_utils.fields
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PageNode',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('created', model_utils.fields.AutoCreatedField(editable=False, verbose_name='created', default=django.utils.timezone.now)),
                ('modified', model_utils.fields.AutoLastModifiedField(editable=False, verbose_name='modified', default=django.utils.timezone.now)),
                ('status', model_utils.fields.StatusField(max_length=100, verbose_name='status', default='draft', choices=[('draft', 'draft'), ('published', 'published')], no_check_for_status=True)),
                ('status_changed', model_utils.fields.MonitorField(verbose_name='status changed', default=django.utils.timezone.now, monitor='status')),
                ('lang', models.CharField(max_length=20, blank=True, verbose_name='language', choices=settings.LANGUAGES)),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('slug', models.SlugField(max_length=255, verbose_name='Slug')),
                ('description', models.CharField(max_length=139, help_text='Description (for Metatag/seo)', blank=True, verbose_name='Description')),
                ('classes', models.CharField(max_length=512, verbose_name='Classes', blank=True, null=True)),
                ('content_type_pk', models.SmallIntegerField(blank=True)),
            ],
            options={
                'verbose_name': 'Node',
                'verbose_name_plural': 'Nodes',
            },
        ),
        migrations.CreateModel(
            name='PageNodePos',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('position', models.PositiveIntegerField()),
                ('content', models.ForeignKey(to='sections.PageNode')),
                ('owner', models.ForeignKey(related_name='in_group', to='sections.PageNode')),
            ],
            options={
                'verbose_name': 'Content Position',
                'verbose_name_plural': 'Content Positions',
                'ordering': ['position'],
            },
        ),
        migrations.AddField(
            model_name='pagenode',
            name='in_nodes',
            field=models.ManyToManyField(related_name='positioned_content', to='sections.PageNode', through='sections.PageNodePos'),
        ),
    ]
