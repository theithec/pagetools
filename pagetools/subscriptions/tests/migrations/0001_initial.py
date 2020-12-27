# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="CustomSubscriber",
            fields=[
                (
                    "id",
                    models.AutoField(
                        serialize=False,
                        auto_created=True,
                        verbose_name="ID",
                        primary_key=True,
                    ),
                ),
                ("is_activated", models.BooleanField(default=False)),
                ("subscribtion_date", models.DateTimeField(auto_now_add=True)),
                ("failures", models.IntegerField(default=0)),
                ("email", models.EmailField(max_length=254)),
                ("user", models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
