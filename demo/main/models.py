from django.db import models

from pagetools.widgets.models import BaseWidget


class ChoosableTemplateWidget(BaseWidget):

    content = models.TextField("Content")
    template = models.CharField(
        "Template",
        max_length=128,
        choices=[
            ("widgets/baswidget.html", "Base"),
            ("main/specialwidget.html", "Special"),
        ],
    )

    def get_template_name(self, context):
        return self.template
