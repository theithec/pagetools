========
Sections
========

Introducion
-----------

This app ist for (rendering) nested content. 


Example
-------

::

    from pagetools.sections.models import TypeMixin, PageNode, PageNodeManager

    class Row(PageNode):
        content = models.TextField("Content")
        teaser = models.TextField("Teaser")
        allowed_children_classes = ["main.models.Article",]
        objects = PageNodeManager()

        def get_absolute_url(self):
            return reverse("main:article", kwargs={'slug': self.slug,})


    class Section(TypeMixin, PageNode):
        node_choices = (
            ('section_style1', 'Style 1'),
            ('section_style2', 'Style 2'),
        )
        headline = models.CharField("Headline", max_length=255)
        allowed_children_classes = [Article,]
        objects = PageNodeManager()


    class SectionList(PageNode):
        allowed_children_classes = [Section,]
        objects = PageNodeManager()

