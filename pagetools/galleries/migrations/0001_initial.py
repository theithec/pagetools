# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import django.utils.timezone
import model_utils.fields
import filebrowser.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('created', model_utils.fields.AutoCreatedField(editable=False, default=django.utils.timezone.now, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(editable=False, default=django.utils.timezone.now, verbose_name='modified')),
                ('status', model_utils.fields.StatusField(no_check_for_status=True, default='draft', verbose_name='status', max_length=100, choices=[('draft', 'draft'), ('published', 'published')])),
                ('status_changed', model_utils.fields.MonitorField(monitor='status', default=django.utils.timezone.now, verbose_name='status changed')),
                ('lang', models.CharField(max_length=20, blank=True, verbose_name='language', choices=settings.LANGUAGES)),
                ('title', models.CharField(verbose_name='Title', max_length=255)),
                ('slug', models.SlugField(verbose_name='Slug', max_length=255)),
                ('description', models.CharField(blank=True, help_text='Description (for Metatag/seo)', verbose_name='Description', max_length=139)),
            ],
            options={
                'abstract': False,
                'verbose_name': 'Galleries',
                'verbose_name_plural': 'Galleries',
            },
        ),
        migrations.CreateModel(
            name='GalleryPic',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('created', model_utils.fields.AutoCreatedField(editable=False, default=django.utils.timezone.now, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(editable=False, default=django.utils.timezone.now, verbose_name='modified')),
                ('status', model_utils.fields.StatusField(no_check_for_status=True, default='draft', verbose_name='status', max_length=100, choices=[('draft', 'draft'), ('published', 'published')])),
                ('status_changed', model_utils.fields.MonitorField(monitor='status', default=django.utils.timezone.now, verbose_name='status changed')),
                ('lang', models.CharField(max_length=20, blank=True, verbose_name='language', choices=settings.LANGUAGES)),
                ('title', models.CharField(verbose_name='Title', max_length=255)),
                ('slug', models.SlugField(verbose_name='Slug', max_length=255)),
                ('description', models.CharField(blank=True, help_text='Description (for Metatag/seo)', verbose_name='Description', max_length=139)),
                ('pic', filebrowser.fields.FileBrowseField(blank=True, verbose_name='Image', max_length=200, null=True)),
            ],
            options={
                'verbose_name': 'Titled Pictures',
            },
        ),
        migrations.CreateModel(
            name='PicPos',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
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
