import datetime
from hashlib import sha224 as sha
import smtplib
import string
#from importlib import import_module
from django.core.mail import  get_connection
from django.core.mail.message import EmailMessage
from django.db import models
#from djan)go.db.models import get_model
from django.db.models.loading import get_model

from django.core.urlresolvers import reverse
from django.utils import timezone
from django.utils.crypto import random
from django.utils.http import urlquote
from django.utils.translation import ugettext_lazy as _
from django.db.utils import ProgrammingError
from pagetools.core.models import  LangModel, LangManager
from . import settings as subs_settings

from .base_models import BaseSubscriberMixin


def _mk_key():
    k = "".join([random.choice(string.ascii_letters + string.digits)
                 for x in range(1, 32)])
    try:
        if Subscriber.objects.filter(key=k):
            k = _mk_key()
    except ProgrammingError:
        pass#        k = _mk_key()
    return k


class Subscriber(BaseSubscriberMixin, LangModel):
    key = models.CharField(max_length=32, default=_mk_key)
    email = models.EmailField(unique=True)
    objects = LangManager()
    def activate(self):
        self.is_activated = True
        self.subscribtion_date = datetime.date(1900, 1, 1)
        self.save()

    def mailkey(self):
        return sha(self.get_email().encode('utf-8')).hexdigest()

    def cmd_path(self):
        return "/?mk=".join(
            (urlquote(self.key), urlquote(self.mailkey())))

    def get_email(self):
        return str(self.email)  #.encode('utf-8')

    @classmethod
    def get_subscribers(cls,**kwargs):
        return cls.objects.lfilter(is_activated=True,
                                   lang=kwargs.pop('lang', None))

_subscriber_model = None




# http://djangosnippets.org/snippets/1993/
# django-mailer, django-mail-queue, ... alle doof
#        choices=(
#            (-1, 'SMTP Fail'),
#            (0, 'Queued'),
#            (1, 'Sent OK'),
#            (2, 'Unexpected Error'),
#        ))
class QueuedEmail(LangModel):

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
        modelname = subs_settings.SUBSCRIBER_MODEL
        if modelname == "Subscriber":
            modelname ="subscribe.Subscriber"
        SubsModel = get_model( *modelname.rsplit('.',1))
        kwargs['lang'] = self.lang
        subscribers = SubsModel.get_subscribers(**kwargs)

        for s in subscribers:
            SendStatus(
                subscriber=s,
                queued_email=self,
                status=0
            ).save()

    def send_to(self, to, conn, unsubscribe_path):
        status = -1
        if self.senddate < timezone.now():
            if self.subject and self.body:
                if to:
                    try:
                        msg = EmailMessage(
                            "%s" % self.subject,
                            self.body.replace('_unsubscribe_path_',
                                              'unsubscribe/%s' % unsubscribe_path),
                            subs_settings.NEWS_FROM,
                            [to],
                            connection=conn,
                        )
                        msg.content_subtype = "html"  # Main content is now text/html
                        status = msg.send( fail_silently=True,)
                    except smtplib.SMTPException:
                        pass
        return status

    # @todo use one connection
    def send_to_all(self, sendstatuses):
        if self.senddate < timezone.now():
            conn = get_connection()
            for s in sendstatuses:
                status = self.send_to(
                    s.subscriber.get_email(),
                    conn,
                    "/%s?mk=%s" %(
                        reverse('unsubscribe', kwargs={'key': s.subscriber.key}),
                        s.subscriber.mailkey()
                     )
                )
                if status == 1:
                    if s.subscriber.failures != 0:
                        s.subscriber.failures = 0
                        s.subscriber.save()
                    s.delete()
                else:
                    s.status = status
                    subscriber = s.subscriber
                    subscriber.failures += 1
                    subscriber.save()
                    if subscriber.failures > subs_settings.MAX_FAILURES:
                        SendStatus.objects.filter(subscriber=subscriber).delete()
                        subscriber.delete()
                    else:
                        s.save()

    def __str__(self):
        return self.subject


class SendStatus(models.Model):
    subscriber = models.ForeignKey(subs_settings.SUBSCRIBER_MODEL)
    queued_email = models.ForeignKey(QueuedEmail)
    status = models.IntegerField()

    def __str__(self):
        return "%s  / %s : %s" % (self.subscriber,
                                  self.queued_email,
                                  self.status)

    class Meta:
        verbose_name = 'Status'
        verbose_name_plural = 'Statuses'
