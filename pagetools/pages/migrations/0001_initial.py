# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import model_utils.fields
import django.utils.timezone
from django.conf import settings

class Migration(migrations.Migration):

    dependencies = [
        ('widgets', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('created', model_utils.fields.AutoCreatedField(editable=False, verbose_name='created', default=django.utils.timezone.now)),
                ('modified', model_utils.fields.AutoLastModifiedField(editable=False, verbose_name='modified', default=django.utils.timezone.now)),
                ('status', model_utils.fields.StatusField(max_length=100, no_check_for_status=True, verbose_name='status', default='draft', choices=[('draft', 'draft'), ('published', 'published')])),
                ('status_changed', model_utils.fields.MonitorField(monitor='status', verbose_name='status changed', default=django.utils.timezone.now)),
                ('lang', models.CharField(max_length=20, blank=True, verbose_name='language', choices=settings.LANGUAGES)),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('slug', models.SlugField(max_length=255, verbose_name='Slug')),
                ('included_form', models.CharField(max_length=255, blank=True, verbose_name='Included form')),
                ('login_required', models.BooleanField(verbose_name='Login required', default=False)),
                ('content', models.TextField(verbose_name='Content')),
                ('pagetype', models.ForeignKey(null=True, to='widgets.PageType', blank=True)),
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
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('field_type', models.CharField(max_length=128, verbose_name='Type')),
                ('name', models.CharField(max_length=512, verbose_name='Name')),
                ('required', models.BooleanField(verbose_name='required', default=False)),
                ('position', models.PositiveSmallIntegerField(verbose_name='Position')),
                ('help_text', models.CharField(max_length=512, blank=True, verbose_name='Helptext')),
                ('initial', models.CharField(max_length=512, blank=True, verbose_name='Default')),
                ('form_containing_model', models.ForeignKey(to='pages.Page', related_name='dynformfields')),
            ],
            options={
                'verbose_name': 'Dynamic Form Field',
                'abstract': False,
                'verbose_name_plural': 'Dynamic Form Fields',
                'ordering': ['position'],
            },
        ),
    ]
