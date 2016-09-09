from django.db import models

from pagetools.widgets.models import BaseWidget


class Article(PageNode):
    content = models.TextField("Content")
    teaser = models.TextField("Teaser")
    image = FileBrowseField("Image",max_length=200)
    allowed_children_classes = ["main.models.Article", "main.models.SectionList"]
    objects = PageNodeManager()

    content = models.TextField('Content')
    template = models.CharField(
        "Template",
        max_length=128,
        choices=[
            ("widgets/baswidget.html", "Base"),
            ("main/specialwidget.html", "Special")]
    )

    def get_template_name(self, context):
        return self.template
