# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

from pagetools.widgets.models import TemplateTagWidget

class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContentWidget',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=128)),
                ('name', models.SlugField(unique=True, verbose_name='name')),
                ('content', models.TextField(verbose_name='Content')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PageType',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(verbose_name='Name', max_length=128)),
                ('parent', models.ForeignKey(blank=True, to='widgets.PageType', null=True)),
            ],
            options={
                'verbose_name': 'Pagetype',
            },
        ),
        migrations.CreateModel(
            name='TemplateTagWidget',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=128)),
                ('name', models.SlugField(unique=True, verbose_name='name')),
                ('renderclasskey', models.CharField(choices=TemplateTagWidget.key_choices, max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TypeArea',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('lang', models.CharField(blank=True, verbose_name='language', max_length=20, choices=[('af', 'Afrikaans'), ('ar', 'Arabic'), ('ast', 'Asturian'), ('az', 'Azerbaijani'), ('bg', 'Bulgarian'), ('be', 'Belarusian'), ('bn', 'Bengali'), ('br', 'Breton'), ('bs', 'Bosnian'), ('ca', 'Catalan'), ('cs', 'Czech'), ('cy', 'Welsh'), ('da', 'Danish'), ('de', 'German'), ('el', 'Greek'), ('en', 'English'), ('en-au', 'Australian English'), ('en-gb', 'British English'), ('eo', 'Esperanto'), ('es', 'Spanish'), ('es-ar', 'Argentinian Spanish'), ('es-mx', 'Mexican Spanish'), ('es-ni', 'Nicaraguan Spanish'), ('es-ve', 'Venezuelan Spanish'), ('et', 'Estonian'), ('eu', 'Basque'), ('fa', 'Persian'), ('fi', 'Finnish'), ('fr', 'French'), ('fy', 'Frisian'), ('ga', 'Irish'), ('gl', 'Galician'), ('he', 'Hebrew'), ('hi', 'Hindi'), ('hr', 'Croatian'), ('hu', 'Hungarian'), ('ia', 'Interlingua'), ('id', 'Indonesian'), ('io', 'Ido'), ('is', 'Icelandic'), ('it', 'Italian'), ('ja', 'Japanese'), ('ka', 'Georgian'), ('kk', 'Kazakh'), ('km', 'Khmer'), ('kn', 'Kannada'), ('ko', 'Korean'), ('lb', 'Luxembourgish'), ('lt', 'Lithuanian'), ('lv', 'Latvian'), ('mk', 'Macedonian'), ('ml', 'Malayalam'), ('mn', 'Mongolian'), ('mr', 'Marathi'), ('my', 'Burmese'), ('nb', 'Norwegian Bokmal'), ('ne', 'Nepali'), ('nl', 'Dutch'), ('nn', 'Norwegian Nynorsk'), ('os', 'Ossetic'), ('pa', 'Punjabi'), ('pl', 'Polish'), ('pt', 'Portuguese'), ('pt-br', 'Brazilian Portuguese'), ('ro', 'Romanian'), ('ru', 'Russian'), ('sk', 'Slovak'), ('sl', 'Slovenian'), ('sq', 'Albanian'), ('sr', 'Serbian'), ('sr-latn', 'Serbian Latin'), ('sv', 'Swedish'), ('sw', 'Swahili'), ('ta', 'Tamil'), ('te', 'Telugu'), ('th', 'Thai'), ('tr', 'Turkish'), ('tt', 'Tatar'), ('udm', 'Udmurt'), ('uk', 'Ukrainian'), ('ur', 'Urdu'), ('vi', 'Vietnamese'), ('zh-cn', 'Simplified Chinese'), ('zh-hans', 'Simplified Chinese'), ('zh-hant', 'Traditional Chinese'), ('zh-tw', 'Traditional Chinese')])),
                ('area', models.CharField(max_length=64, choices=[('sidebar', 'Sidebar')])),
                ('type', models.ForeignKey(to='widgets.PageType')),
            ],
            options={
                'verbose_name_plural': 'Pagetype-Areas',
                'verbose_name': 'Pagetype-Area',
            },
        ),
        migrations.CreateModel(
            name='WidgetInArea',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('position', models.PositiveIntegerField()),
                ('enabled', models.BooleanField(default=False, verbose_name='enabled')),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('typearea', models.ForeignKey(related_name='widgets', to='widgets.TypeArea')),
            ],
            options={
                'ordering': ['position'],
            },
        ),
        migrations.AlterUniqueTogether(
            name='typearea',
            unique_together=set([('area', 'type', 'lang')]),
        ),
    ]
