# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django
from django.db import migrations, models

import pagetools.models


class Migration(migrations.Migration):

    dependencies = [
        ("sections", "0004_auto_20160918_2055"),
    ]
    if django.VERSION < (1, 9):
        operations = [
            migrations.AlterField(
                model_name="pagenode",
                name="slug",
                field=pagetools.models._USlugField(verbose_name="Slug", max_length=255),
            ),
        ]
