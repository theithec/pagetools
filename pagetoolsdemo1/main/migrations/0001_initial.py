# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sections', '0002_auto_20160120_2021'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('pagenode_ptr', models.OneToOneField(to='sections.PageNode', auto_created=True, serialize=False, primary_key=True, parent_link=True)),
                ('content', models.TextField(verbose_name='Content')),
            ],
            options={
                'abstract': False,
            },
            bases=('sections.pagenode',),
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('pagenode_ptr', models.OneToOneField(to='sections.PageNode', auto_created=True, serialize=False, primary_key=True, parent_link=True)),
                ('node_type', models.CharField(max_length=128, blank=True)),
            ],
            options={
                'verbose_name': 'Section',
                'verbose_name_plural': 'Sections',
            },
            bases=('sections.pagenode', models.Model),
        ),
        migrations.CreateModel(
            name='SectionPage',
            fields=[
            ],
            options={
                'verbose_name': 'Page',
                'verbose_name_plural': 'Pages',
                'proxy': True,
            },
            bases=('sections.pagenode',),
        ),
    ]
