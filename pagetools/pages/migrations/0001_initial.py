# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import model_utils.fields
import django.utils.timezone


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
                ('lang', models.CharField(max_length=20, blank=True, verbose_name='language', choices=[('af', 'Afrikaans'), ('ar', 'Arabic'), ('ast', 'Asturian'), ('az', 'Azerbaijani'), ('bg', 'Bulgarian'), ('be', 'Belarusian'), ('bn', 'Bengali'), ('br', 'Breton'), ('bs', 'Bosnian'), ('ca', 'Catalan'), ('cs', 'Czech'), ('cy', 'Welsh'), ('da', 'Danish'), ('de', 'German'), ('el', 'Greek'), ('en', 'English'), ('en-au', 'Australian English'), ('en-gb', 'British English'), ('eo', 'Esperanto'), ('es', 'Spanish'), ('es-ar', 'Argentinian Spanish'), ('es-mx', 'Mexican Spanish'), ('es-ni', 'Nicaraguan Spanish'), ('es-ve', 'Venezuelan Spanish'), ('et', 'Estonian'), ('eu', 'Basque'), ('fa', 'Persian'), ('fi', 'Finnish'), ('fr', 'French'), ('fy', 'Frisian'), ('ga', 'Irish'), ('gl', 'Galician'), ('he', 'Hebrew'), ('hi', 'Hindi'), ('hr', 'Croatian'), ('hu', 'Hungarian'), ('ia', 'Interlingua'), ('id', 'Indonesian'), ('io', 'Ido'), ('is', 'Icelandic'), ('it', 'Italian'), ('ja', 'Japanese'), ('ka', 'Georgian'), ('kk', 'Kazakh'), ('km', 'Khmer'), ('kn', 'Kannada'), ('ko', 'Korean'), ('lb', 'Luxembourgish'), ('lt', 'Lithuanian'), ('lv', 'Latvian'), ('mk', 'Macedonian'), ('ml', 'Malayalam'), ('mn', 'Mongolian'), ('mr', 'Marathi'), ('my', 'Burmese'), ('nb', 'Norwegian Bokmal'), ('ne', 'Nepali'), ('nl', 'Dutch'), ('nn', 'Norwegian Nynorsk'), ('os', 'Ossetic'), ('pa', 'Punjabi'), ('pl', 'Polish'), ('pt', 'Portuguese'), ('pt-br', 'Brazilian Portuguese'), ('ro', 'Romanian'), ('ru', 'Russian'), ('sk', 'Slovak'), ('sl', 'Slovenian'), ('sq', 'Albanian'), ('sr', 'Serbian'), ('sr-latn', 'Serbian Latin'), ('sv', 'Swedish'), ('sw', 'Swahili'), ('ta', 'Tamil'), ('te', 'Telugu'), ('th', 'Thai'), ('tr', 'Turkish'), ('tt', 'Tatar'), ('udm', 'Udmurt'), ('uk', 'Ukrainian'), ('ur', 'Urdu'), ('vi', 'Vietnamese'), ('zh-cn', 'Simplified Chinese'), ('zh-hans', 'Simplified Chinese'), ('zh-hant', 'Traditional Chinese'), ('zh-tw', 'Traditional Chinese')])),
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
