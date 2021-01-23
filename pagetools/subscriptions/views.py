import datetime
from hashlib import sha224 as sha
from smtplib import SMTPException

from django import apps, template
from django.contrib import messages
from django.contrib.sites.models import Site
from django.core.mail import EmailMultiAlternatives

from django.http.response import Http404, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import get_language
from django.utils.translation import ugettext_lazy as _

from . import settings as subs_settings
from .models import Subscriber

config = apps.apps.get_app_config("subscriptions")
subscribe_form = config.subscribe_form


def _send_mail(subscriber, template_name, context, subject, attachmentfile=None):
    tmpl = template.loader.get_template(template_name + ".txt")
    msg = tmpl.render(context)
    try:
        tmpl = template.loader.get_template(template_name + ".html")
        htmlmsg = tmpl.render(context)
    except template.exceptions.TemplateDoesNotExist:
        htmlmsg = None
    email = EmailMultiAlternatives(subject, msg, subs_settings.NEWS_FROM, [subscriber.email])
    if htmlmsg:
        email.attach_alternative(htmlmsg, "text/html")
    if attachmentfile:
        email.attach_file(attachmentfile)
    try:
        email.send()
    except SMTPException:
        return False

    return True  # send_mail


def _send_activation_mail(subscriber, template_name):
    site_url = "https://%s" % Site.objects.get_current().domain
    context = {
        "site_name": Site.objects.get_current().name,
        "site_url": site_url,
        "activation_url": "%s%s?mk=%s/"
        % (
            site_url,
            (reverse("subscriptions:activate", kwargs={"key": subscriber.key})),
            subscriber.mailkey(),
        ),
    }
    subject = subs_settings.ACTIVATION_MAIL_SUBJECT
    return _send_mail(subscriber, template_name, context, subject)


def _subscribe(request, mail_success_template_name="subscriptions/activation_msg"):
    msg = _("An error occurred")
    form = subscribe_form(request.POST)
    errors = True
    if form.is_valid():
        clean_data = form.clean()
        email = clean_data["email"]
        already_there = Subscriber.objects.filter(email=email).exists()
        subs_msg = _("subscribed: %s") % email
        if not already_there:
            subscriber = Subscriber(email=email, is_activated=False, lang=get_language())
            mail_success = _send_activation_mail(subscriber, mail_success_template_name)
            if mail_success:
                subscriber.save()
        if already_there or mail_success:
            msg = subs_msg
            errors = False
    else:
        msg = str(form.errors)
    return msg, errors


def _subscribe_fallback(request, msg, errors):
    # messages.add_message(request, messages.ERROR if errors else messages.SUCCESS, msg)
    return render(
        request,
        "subscriptions/subscribe_msg.html",
    )


def _subscribe_json(msg, errors):
    return JsonResponse({"msg": msg, "errors": errors})


def subscribe(request):
    if request.method == "GET":
        raise Http404
    msg, errors = _subscribe(request)
    if request.is_ajax():
        return _subscribe_json(msg, errors)
    messages.add_message(request, messages.SUCCESS, msg)
    return _subscribe_fallback(request, msg, errors)


def _matching_activated_subscriber(request, key):
    # remove trailing slash
    mailkey = request.GET.get("mk", "/")[:-1]
    subscriber = get_object_or_404(Subscriber, key=key)
    mailsha = sha(subscriber.email.encode("utf-8")).hexdigest()
    if mailsha == mailkey:
        return subscriber
    return None


def _activate(request, key):
    subscriber = _matching_activated_subscriber(request, key)
    if subscriber:
        activate_end = subscriber.subscribtion_date + datetime.timedelta(hours=48)
        if not subscriber.is_activated and activate_end > timezone.now():
            subscriber.activate()
            messages.add_message(request, messages.SUCCESS, _("activation: ok"))
            return subscriber


def activate(request, key):
    if _activate(request, key):
        return render(request, subs_settings.MSG_BASE_TEMPLATE)  # , {"msg": _("activation: ok")}
    raise Http404()


def unsubscribe(request, key):
    subscriber = _matching_activated_subscriber(request, key)
    if subscriber and subscriber.is_activated:
        subscriber.delete()
        messages.add_message(request, messages.SUCCESS, _("unsubscribe: ok"))
        return render(request, subs_settings.MSG_BASE_TEMPLATE, {"msg": _("unsubscribe: ok")})
    raise Http404()
