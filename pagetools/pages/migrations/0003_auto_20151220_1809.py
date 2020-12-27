# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pages", "0002_page_pagetype"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="pagedynformfield",
            options={
                "verbose_name": "Form field",
                "verbose_name_plural": "Additional form fields",
            },
        ),
        migrations.AddField(
            model_name="page",
            name="email_receivers",
            field=models.CharField(
                blank=True,
                help_text="Comma separated list of emails",
                verbose_name="Email Receivers",
                max_length=512,
            ),
        ),
        migrations.AlterField(
            model_name="pagedynformfield",
            name="field_type",
            field=models.CharField(
                help_text="The type of the field (e.g. textfield)",
                verbose_name="Type",
                max_length=128,
            ),
        ),
        migrations.AlterField(
            model_name="pagedynformfield",
            name="form_containing_model",
            field=models.ForeignKey(
                help_text="Additional fields and settings for the included form",
                related_name="dynformfields",
                to="pages.Page",
                on_delete=models.CASCADE,
            ),
        ),
        migrations.AlterField(
            model_name="pagedynformfield",
            name="help_text",
            field=models.CharField(
                blank=True,
                help_text="The helptext of the field ",
                verbose_name="Helptext",
                max_length=512,
            ),
        ),
        migrations.AlterField(
            model_name="pagedynformfield",
            name="initial",
            field=models.CharField(
                blank=True,
                help_text="The default value of the field",
                verbose_name="Default",
                max_length=512,
            ),
        ),
        migrations.AlterField(
            model_name="pagedynformfield",
            name="name",
            field=models.CharField(
                help_text="The visible name of the field",
                verbose_name="Value",
                max_length=512,
            ),
        ),
        migrations.AlterField(
            model_name="pagedynformfield",
            name="required",
            field=models.BooleanField(
                help_text="Is the field required?",
                verbose_name="required",
                default=False,
            ),
        ),
    ]
