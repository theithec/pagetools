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
            name='Page',
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
                ('included_form', models.CharField(max_length=255, verbose_name='Included form', blank=True)),
                ('login_required', models.BooleanField(verbose_name='Login required', default=False)),
                ('content', models.TextField(verbose_name='Content')),
            ],
            options={
                'verbose_name': 'Page',
                'abstract': False,
                'verbose_name_plural': 'Pages',
            },
        ),
        migrations.CreateModel(
            name='PageDynFormField',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('field_type', models.CharField(max_length=128, verbose_name='Type')),
                ('name', models.CharField(max_length=512, verbose_name='Value')),
                ('required', models.BooleanField(verbose_name='required', default=False)),
                ('position', models.PositiveSmallIntegerField(verbose_name='Position')),
                ('help_text', models.CharField(max_length=512, verbose_name='Helptext', blank=True)),
                ('initial', models.CharField(max_length=512, verbose_name='Default', blank=True)),
                ('form_containing_model', models.ForeignKey(related_name='dynformfields', to='pages.Page')),
            ],
            options={
                'verbose_name': 'Dynamic Form Field',
                'abstract': False,
                'verbose_name_plural': 'Dynamic Form Fields',
                'ordering': ['position'],
            },
        ),
    ]
