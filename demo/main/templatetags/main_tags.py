from django import template
from django.utils.datetime_safe import datetime

from main.models import News


# Time Example from
# https://docs.djangoproject.com/en/dev/howto/custom-template-tags/
class CurrentTimeNode(template.Node):
    def __init__(self, format_string='%Y-%m-%d %I:%M %p'):
        self.format_string = format_string

    def render(self, context):
        return datetime.datetime.now().strftime(self.format_string)


def do_current_time(parser, token):
    try:
        # split_contents() knows not to split quoted strings.
        tag_name, format_string = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            "%r tag requires a single argument" % token.contents.split()[0])
    if not (format_string[0] == format_string[-1] and
            format_string[0] in ('"', "'")):
        raise template.TemplateSyntaxError(
            "%r tag's argument should be in quotes" % tag_name)
    return CurrentTimeNode(format_string[1:-1])


class NewsMonthNode(template.Node):
    def render(self, context):
        news = News.public.lfilter()
        firstdt = news.first().status_changed
        fy, fm = firstdt.year, firstdt.month

        lastdt = news.last().status_changed
        ly, lm = lastdt.year, lastdt.month
        txt = '<ol class="list-unstyled">'
        cy = fy
        cm = fm
        while (cy < ly or (cy == ly and cm <= lm)):
            mn = datetime(year=cy, month=cm, day=1)
            txt += '<li><a href="/%s/%s">%s %s</a></li>' % (
                cy, mn.strftime("%b"),
                mn.strftime("%B"), cy)
            # print cy,cm, "(%s,  %s)" % (lm, ly)
            cm += 1
            if cm == 13:
                cm = 1
                cy += 1
        txt += "</ul>"
        return txt
