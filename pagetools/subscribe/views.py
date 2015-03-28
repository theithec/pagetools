# -*- coding: utf-8 -*-
# Create your views here.

import datetime
from hashlib import sha224 as sha
import json
from smtplib import SMTPException

from django import template
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.http.response import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.template.context import Context
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.contrib.sites.models import Site
from pagetools.subscribe.forms import SubscribeForm
from pagetools.subscribe.models import Subscriber

from . import settings as subs_settings


def _subscribe(request):
    msg = _("An error occurred")
    form = SubscribeForm(request.POST)
    if form.is_valid():
        clean_data = form.clean()
        email = clean_data['email']
        already_there = Subscriber.objects.filter(email=email)
        subs_msg = _('subscribed: %s') % email
        if not already_there:
            s = Subscriber(email=email, is_activated=False)
            site_url = "https://%s" % Site.objects.get_current().domain
            context = {
                'site_name': Site.objects.get_current().name,
                'site_url': site_url,
                'activation_url': "%s%s?mk=%s/" % (
                    site_url,
                    (reverse('activate', kwargs={'key': s.key})),
                    s.mailkey()
                )
            }
            t = template.loader.get_template('subscribe/activation_msg.txt')
            mailmsg = t.render(Context(context))
            try:
                send_mail(
                    subs_settings.ACTIVATION_MAIL_SUBJECT,
                    mailmsg,
                    subs_settings.NEWS_FROM,
                    [form['email'].value()],
                    fail_silently=False
                    )
                s.save()
                msg = subs_msg
            except SMTPException:
                pass
        else:
            msg = subs_msg
    else:
        msg = str(form.errors)
    return msg


def _subscribe_fallback(request, c):
    c['referer'] = request.META.get('HTTP_REFERER', '/')
    return render(
        request,
        'subscribe/subscribe_msg.html',
    )


def _subscribe_json(msg):
    return HttpResponse( json.dumps({'msg':str(msg['msg'])}))


def subscribe(request):
    c = {}
    c['msg'] = _subscribe(request)
    if request.is_ajax():
        return _subscribe_json(c)
    return _subscribe_fallback(request, c)


def _matching_activated_subscriber(request, key):
    # remove trailing slash
    mailkey = request.GET.get('mk', '/')[:-1]
    s = get_object_or_404(Subscriber, key=key)
    mailsha = sha(s.email.encode('utf-8')).hexdigest()
    if mailsha == mailkey:
        return s
    return None


def activate(request, key):
    s = _matching_activated_subscriber(request, key)
    activate_end = s.subscribtion_date + datetime.timedelta(hours=48)
    if s and not s.is_activated and activate_end > timezone.now():
        s.activate()
        return render(request, subs_settings.MSG_BASE_TEMPLATE,
                      {'msg': _('activation: ok')}
                      )
    raise Http404()


def unsubscribe(request, key):
    s = _matching_activated_subscriber(request, key)
    if s and s.is_activated:
        s.delete()
        return render(request,
                      subs_settings.MSG_BASE_TEMPLATE,
                      {'msg': _('unsubscribe: ok')})
