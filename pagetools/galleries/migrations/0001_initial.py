# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import filebrowser.fields
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(editable=False, verbose_name='created', default=django.utils.timezone.now)),
                ('modified', model_utils.fields.AutoLastModifiedField(editable=False, verbose_name='modified', default=django.utils.timezone.now)),
                ('status', model_utils.fields.StatusField(choices=[('draft', 'draft'), ('published', 'published')], verbose_name='status', max_length=100, no_check_for_status=True, default='draft')),
                ('status_changed', model_utils.fields.MonitorField(verbose_name='status changed', default=django.utils.timezone.now, monitor='status')),
                ('lang', models.CharField(max_length=20, blank=True, verbose_name='language', choices=settings.LANGUAGES)),
                ('title', models.CharField(verbose_name='Title', max_length=255)),
                ('slug', models.SlugField(verbose_name='Slug', max_length=255)),
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
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(editable=False, verbose_name='created', default=django.utils.timezone.now)),
                ('modified', model_utils.fields.AutoLastModifiedField(editable=False, verbose_name='modified', default=django.utils.timezone.now)),
                ('status', model_utils.fields.StatusField(choices=[('draft', 'draft'), ('published', 'published')], verbose_name='status', max_length=100, no_check_for_status=True, default='draft')),
                ('status_changed', model_utils.fields.MonitorField(verbose_name='status changed', default=django.utils.timezone.now, monitor='status')),
                ('lang', models.CharField(max_length=20, blank=True, verbose_name='language', choices=settings.LANGUAGES)),
                ('title', models.CharField(verbose_name='Title', max_length=255)),
                ('slug', models.SlugField(verbose_name='Slug', max_length=255)),
                ('pic', filebrowser.fields.FileBrowseField(verbose_name='Image', max_length=200, blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Titled Pictures',
            },
        ),
        migrations.CreateModel(
            name='PicPos',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
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
            field=models.ManyToManyField(through='galleries.PicPos', to='galleries.GalleryPic'),
        ),
    ]
