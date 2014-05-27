import datetime
from hashlib import sha224 as sha
import smtplib
import string
import imp
from django.core.mail import send_mail, get_connection
from django.db import models
from django.db.models import get_model
from django.utils import timezone
from django.utils.crypto import random
from django.utils.http import urlquote
from django.utils.translation import ugettext_lazy as _

import settings as subs_settings

from .base_models import BaseSubscriberMixin


def _mk_key():
    k = "".join([random.choice(string.letters + string.digits)
                 for x in range(1, 32)])
    if Subscriber.objects.filter(key=k):
        k = _mk_key()
    return k


class Subscriber(BaseSubscriberMixin):
    key = models.CharField(max_length=32, default=_mk_key)
    email = models.EmailField(unique=True)

    def activate(self):
        self.is_activated = True
        # self.key = '-'
        self.subscribtion_date = datetime.date(1900, 1, 1)
        self.save()

    def mailkey(self):
        return sha(self.get_email()).hexdigest()

    def cmd_path(self):
        return "/?mk=".join(
                    (urlquote(self.key), urlquote(self.mailkey())))

    def get_email(self):
        return self.email


_subscriber_model = None


def get_subscriber_model():

    global _subscriber_model
    if not _subscriber_model:
        modulename, clsname = subs_settings.SUBSCRIBER_MODEL
        if modulename == "pagetools.subscribe":
            _subscriber_model = Subscriber
        else:
            _subscriber_model = get_model(modulename, clsname)
    # print "SUBSRIBER_MODEL", _subscriber_model
    return _subscriber_model


# http://djangosnippets.org/snippets/1993/
# django-mailer, django-mail-queue, ... alle doof
#        choices=(
#            (-1, 'SMTP Fail'),
#            (0, 'Queued'),
#            (1, 'Sent OK'),
#            (2, 'Unexpected Error'),
#        ))
class QueuedEmail(models.Model):

    class Meta:
        abstract = False
        verbose_name = _("News-Mail")

    createdate = models.DateTimeField('Created on',
        default=timezone.now(),
        blank=True,
        editable=False)

    modifydate = models.DateTimeField('Last modified on',
        default=timezone.now(),
        blank=True,
        editable=False)

    senddate = models.DateTimeField('Send after',
        default=timezone.now(),
        blank=True,
        editable=True)

    subject = models.CharField(verbose_name="Subject",
        default="",
        unique=False,
        blank=True,
        max_length=255)

    body = models.TextField(verbose_name="Body",
        default="",
        unique=False,
        blank=True)

    def save(self, force_insert=False, force_update=False, **kwargs):
        self.modifydate = timezone.now()
        super(QueuedEmail, self).save(force_insert, force_update)
        SubsModel = get_subscriber_model()
        subscribers = SubsModel.objects.filter(is_activated=True)
        for s in subscribers:
            SendStatus(
                subscriber=s,
                queued_email=self,
                status=0
            ).save()

    def send_to(self, to, conn, unsubscribe_path):
        if self.senddate < timezone.now():
            if self.subject and self.body:
                if to:
                    try:
                        status = send_mail(
                            "%s" % self.subject,
                            self.body.replace('%unsubscribe_path%',
                                              unsubscribe_path),
                            subs_settings.NEWS_FROM,
                            [to],
                            connection=conn,
                            fail_silently=False
                        )
                    except smtplib.SMTPException:
                        status = -1
        return status

    # @todo use one connection
    def send_to_all(self, sendstatuses):
        if self.senddate < timezone.now():
            conn = get_connection()
            for s in sendstatuses:
                status = self.send_to(s.subscriber.get_email(),
                                      conn,
                                      s.subscriber.cmd_path())
                if status == 1:
                    s.subscriber.failures = 0
                    # s.subscriber.save() #?
                    s.delete()
                else:
                    s.status = status
                    subscriber = s.subscriber
                    subscriber.failures += 1
                    if subscriber.failures > subs_settings.MAX_FAILURES:
                        SendStatus.objects.filter(subscriber=subscriber).delete()
                        subscriber.delete()
                    else:
                        s.save()

    def __unicode__(self):
        return self.subject


class SendStatus(models.Model):
    subscriber = models.ForeignKey(get_subscriber_model())
    queued_email = models.ForeignKey(QueuedEmail)
    status = models.IntegerField()

    def __unicode__(self):
        return "%s  / %s : %s" % (self.subscriber,
                                  self.queued_email,
                                  self.status)

    class Meta:
        verbose_name = 'Status'
        verbose_name_plural = 'Statuses'
