# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings

def is_test_db():
    from django.db import connection
    print("S", connection.settings_dict)
    db_name = connection.settings_dict['NAME']
    return db_name.startswith("file:memorydb")
    return settings.DATABASES.get(
        'default', {}).get('NAME', '').startswith('test_')

class Migration(migrations.Migration):

    dependencies = [
        ('sections', '0002_auto_20160120_2021'),
    ]
    print("IS TEST", is_test_db())
    if is_test_db():
        operations = [
            migrations.CreateModel(
                name='TestNode',
                fields=[
                    ('pagenode_ptr', models.OneToOneField(to='sections.PageNode', parent_link=True, serialize=False, auto_created=True, primary_key=True)),
                ],
                options={
                    'abstract': False,
                },
                bases=('sections.pagenode',),
            ),
        ]
