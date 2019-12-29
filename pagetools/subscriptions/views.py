import datetime
from hashlib import sha224 as sha
from smtplib import SMTPException

from django import template, apps
from django.core.mail import send_mail
from django.urls import reverse
from django.http.response import Http404, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.utils.translation import get_language, ugettext_lazy as _
from django.contrib.sites.models import Site
from django.contrib import messages
from .forms import SubscribeForm
from .models import Subscriber

from . import settings as subs_settings

config = apps.apps.get_app_config("subscriptions")
subscribe_form = config.subscribe_form


def _send_activation_mail(subscriber):
    site_url = "https://%s" % Site.objects.get_current().domain
    context = {
        'site_name': Site.objects.get_current().name,
        'site_url': site_url,
        'activation_url': "%s%s?mk=%s/" % (
            site_url,
            (reverse('subscriptions:activate', kwargs={'key': subscriber.key})),
            subscriber.mailkey()
        )
    }
    tmpl = template.loader.get_template('subscriptions/activation_msg.txt')
    mailmsg = tmpl.render(context)
    try:
        send_mail(
            subs_settings.ACTIVATION_MAIL_SUBJECT,
            mailmsg,
            subs_settings.NEWS_FROM,
            [subscriber.email],
            fail_silently=False
        )
    except SMTPException:
        return False

    return True #send_mail


def _subscribe(request):
    msg = _("An error occurred")
    form = subscribe_form(request.POST)
    errors = True
    if form.is_valid():
        clean_data = form.clean()
        email = clean_data['email']
        already_there = Subscriber.objects.filter(email=email)
        subs_msg = _('subscribed: %s') % email
        if not already_there:
            subscriber = Subscriber(email=email, is_activated=False, lang=get_language())
            mail_success = _send_activation_mail(subscriber)
            if mail_success:
                subscriber.save()
        if already_there or mail_success:
            msg = subs_msg
            errors = False
    else:
        msg = str(form.errors)
    return msg, errors


def _subscribe_fallback(request, msg, errors):
    messages.add_message(request, messages.ERROR if errors else messages.SUCCESS, msg)
    return render(
        request,
        'subscriptions/subscribe_msg.html',
    )


def _subscribe_json(msg, errors):
    return JsonResponse({"msg": msg, "errors": errors})


def subscribe(request):
    if request.method == 'GET':
        raise Http404
    msg, errors = _subscribe(request)
    # ups, lazy
    # res['msg'] = '%s' % res['msg']
    if request.is_ajax():
        return _subscribe_json(msg, errors)

    messages.add_message(request, messages.INFO, msg)
    return _subscribe_fallback(request, msg, errors)


def _matching_activated_subscriber(request, key):
    # remove trailing slash
    mailkey = request.GET.get('mk', '/')[:-1]
    subscriber = get_object_or_404(Subscriber, key=key)
    mailsha = sha(subscriber.email.encode('utf-8')).hexdigest()
    if mailsha == mailkey:
        return subscriber
    return None


def activate(request, key):
    subscriber = _matching_activated_subscriber(request, key)
    activate_end = subscriber.subscribtion_date + datetime.timedelta(hours=48)
    if subscriber and not subscriber.is_activated and activate_end > timezone.now():
        subscriber.activate()
        messages.add_message(request, messages.INFO, _('activation: ok'))

        return render(request, subs_settings.MSG_BASE_TEMPLATE,
                      {'msg': _('activation: ok')})
    raise Http404()


def unsubscribe(request, key):
    subscriber = _matching_activated_subscriber(request, key)
    if subscriber and subscriber.is_activated:
        subscriber.delete()
        messages.add_message(request, messages.INFO, _('unsubscribe: ok'))

        return render(request,
                      subs_settings.MSG_BASE_TEMPLATE,
                      {'msg': _('unsubscribe: ok')})
    raise Http404()
