import os, sys # noqa

from django.contrib.auth.models import User #noqa
from django.contrib.sites.models import Site
from django.core import management  #noqa
from django.core.management.base import BaseCommand
from django.utils import timezone #noqa

from filebrowser.base import FileObject

import pagetools.menus.utils #noqa


from pagetools.core.settings import STATUS_PUBLISHED #noqa
from pagetools.menus.models import Menu, AutoPopulated, ViewLink #noqa
from pagetools.pages.models import Page #noqa
from pagetools.widgets.models import (PageType,  TypeArea, ContentWidget, # noqa
                                      WidgetInArea, TemplateTagWidget) #noqa

from polls.models import Question, Choice #noqa

from demo_sections.models import Article, Section, SectionList

def create():
    site = Site.objects.first()
    site.domain = "127.0.0.1:8000"
    site.name = "Localhost"
    site.save()
    menu = Menu.objects.add_root("MainMenu")

    pagetype_base = PageType.objects.create(name="base")
    pagetype_special = PageType.objects.create(name="special")

    about_kwargs = {'pagetype': pagetype_special, 'included_form':'Contactform'}
    pages_data = [
        ('Welcome', 'start', "This is the start page"),
        ('About', 'about', "That's a good one.<h3>Any questions?</h3>", about_kwargs),
    ]


    for d in pages_data:
        kwargs = {}
        if len(d) > 3:
            kwargs = d[3]
        page = Page.objects.get_or_create(
            title=d[0],
            slug=d[1],
            content=d[2],
            status=STATUS_PUBLISHED,
            **kwargs
        )[0]
        menu.children.add_child(page, enabled=True)

    print("MENU", menu)
    #  menu = Menu.objects.get(title="MainMenu")


    typearea_base = TypeArea.objects.create(
        area="sidebar", pagetype=pagetype_base)
    typearea_special = TypeArea.objects.create(
        area="sidebar", pagetype=pagetype_special)

    content_widget1 = ContentWidget.objects.create(
        title="Widget1", name="widget1", content="I'm for base")
    content_widget2 = ContentWidget.objects.create(
        title="Widget2", name="widget2", content="I'm special")
    content_widget3 = ContentWidget.objects.create(
        title="Widget3", name="widget3", content="I'm always there")
    management.call_command("mk_templatetagwidgets")
    latest_question_widget = TemplateTagWidget.objects.get(name="latest_question")
    latest_question_widget.title = "Latest Questions"
    latest_question_widget.save()
    subscribe_widget = TemplateTagWidget.objects.get(name="subscribe")

    widgets_areas = (
        (content_widget1, typearea_base),
        (content_widget2, typearea_special),
        (content_widget3, typearea_base),
        (content_widget3, typearea_special),
        (latest_question_widget, typearea_base),
        (subscribe_widget, typearea_base),
    )
    for d in widgets_areas:
        WidgetInArea.objects.create(
            typearea=d[1],
            content_object=d[0],
            position=0,
            enabled=True)


    questions_data = (
        ("What's up?", ["Something maybe", "Nothing"],),
        ("What should i ask?", ["Not sure", "Nothing"],),
    )

    for d in questions_data:
        q = Question.objects.create(question_text=d[0], pub_date=timezone.now())
        for c in d[1]:
            q.choice_set.create(choice_text=c)
    a = AutoPopulated.objects.create(name="All questions")
    menu.children.add_child(a, enabled=True)

    sl1 = SectionList.objects.create(
        title="Sectionlist1", slug="sectionlist1", status=STATUS_PUBLISHED)

    menu.children.add_child(sl1, enabled=True, title="Sections")
    s1 = Section.objects.create(title="Section1", slug="section1",
                                status=STATUS_PUBLISHED )
    pp = s1.pagenodepos_set.create(position=1, content=s1, owner=sl1)

    for i in range(4):
        kwargs = {}
        if i<3:
            kwargs['status'] = STATUS_PUBLISHED
        a = Article.objects.create(
            title="Article %s" % i,
            content="Long version of article %s" % i,
            teaser="Short version of article %s" % i,
            image=FileObject("uploads/pic_10.jpg"),
            slug="article%s" % i,
            **kwargs
        )
        pp = a.pagenodepos_set.create(position=i, content=a, owner=s1)

    vl_polls = ViewLink.objects.create(title="Polls", name="polls:index")
    menu.children.add_child(vl_polls, enabled=True, title="Polls")


class Command(BaseCommand):
    help = 'Creates data for the pagetools demo'

    def handle(self, *args, **options):

        management.call_command("migrate")
        try:
            User.objects.create_superuser("admin", "q@w.de", "pass#word")
        except:
            sys.exit("Error. DB exists?")
        create()



