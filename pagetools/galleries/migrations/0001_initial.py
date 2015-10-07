# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import model_utils.fields
import filebrowser.fields
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Gallery',
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
            ],
            options={
                'verbose_name': 'Galleries',
                'abstract': False,
                'verbose_name_plural': 'Galleries',
            },
        ),
        migrations.CreateModel(
            name='GalleryPic',
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
                ('pic', filebrowser.fields.FileBrowseField(max_length=200, verbose_name='Image', blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Titled Pictures',
            },
        ),
        migrations.CreateModel(
            name='PicPos',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('position', models.PositiveIntegerField()),
                ('gal', models.ForeignKey(to='galleries.Gallery')),
                ('pic', models.ForeignKey(related_name='positioned_pic', to='galleries.GalleryPic')),
            ],
            options={
                'verbose_name': 'Positioned Picture',
            },
        ),
        migrations.AddField(
            model_name='gallery',
            name='pics',
            field=models.ManyToManyField(to='galleries.GalleryPic', through='galleries.PicPos'),
        ),
    ]
