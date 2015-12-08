# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
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
                ('included_form', models.CharField(blank=True, verbose_name='Included form', max_length=255)),
                ('login_required', models.BooleanField(default=False, verbose_name='Login required')),
                ('content', models.TextField(verbose_name='Content')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'Page',
                'verbose_name_plural': 'Pages',
            },
        ),
        migrations.CreateModel(
            name='PageDynFormField',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('field_type', models.CharField(verbose_name='Type', max_length=128)),
                ('name', models.CharField(verbose_name='Value', max_length=512)),
                ('required', models.BooleanField(default=False, verbose_name='required')),
                ('position', models.PositiveSmallIntegerField(verbose_name='Position')),
                ('help_text', models.CharField(blank=True, verbose_name='Helptext', max_length=512)),
                ('initial', models.CharField(blank=True, verbose_name='Default', max_length=512)),
                ('form_containing_model', models.ForeignKey(related_name='dynformfields', to='pages.Page')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'Dynamic Form Field',
                'ordering': ['position'],
                'verbose_name_plural': 'Dynamic Form Fields',
            },
        ),
    ]
