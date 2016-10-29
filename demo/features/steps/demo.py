from behave import *
from django.core.urlresolvers import reverse
import time

from pagetools.pages.models import Page

@given('site has content')
def step_impl(context):
    pass

    #Page.objects.create(
    #    title='Startpage',
    #    slug='start',
    #    content="Start",
    #    status="published"
    #)
    #context.test.assertEqual("/", reverse("index"))
    #r = context.test.client.get(reverse("index"))
    #print("R", r)

@when('i visit the url "{url}"')
def step_impl(context, url):
    print("ALL", Page.objects.all())
    # ocontext.test.assertEqual("http:/127.0.0.1", context.base_url)
    print("LIV", context.test.live_server_url, context.base_url)
    context.browser.get(context.base_url + url)

@then('the title should be "{title}"')
def the_title_should_be(context, title):
    browser_title = context.browser.title # .replace('|', '!')
    context.test.assertEqual(
        browser_title,
        "Polls'n'Pagetools|%s" % title)

