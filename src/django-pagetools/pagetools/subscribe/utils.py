'''
Created on 03.09.2012

@author: lotek
'''

from django import template
from django.contrib.sites.models import Site
from django.template.context import Context

from pagetools.subscribe import settings as subs_settings
from .models import QueuedEmail, SendStatus




def to_queue(content):
    # subscribers = Subscriber.objects.filter(is_activated=True)
    t = template.loader.get_template('subscribe/msg.txt')

    msg = t.render(Context({
        'content': content['body'],
        'site': Site.objects.get_current(),
        'unsubscribe_url':"http://" + Site.objects.get_current().domain + "/subscribe/unsubscribe/"
    }))
    qm = QueuedEmail(
        subject="%s %s" % (subs_settings.NEWS_SUBJECT_PREFIX, content['title']),
        body=msg
    )
    qm.save()


def send_queued_mail(qm, maxmails):
    sts = SendStatus.objects.filter(queued_email=qm)[:maxmails]
    qm.send_to_all(sts)
    sst2 = SendStatus.objects.filter(queued_email=qm)
    if not sst2:
        qm.delete()
    return len(sts)


def send_max(max_send=subs_settings.MAX_PER_TIME):
    qms = QueuedEmail.objects.all()
    num_sended = 0
    for qm in qms:
        maxmails = max_send - num_sended
        if maxmails < 1:
            break
        num_sended += send_queued_mail(qm, maxmails)

# other ideas:   http://stackoverflow.com/questions/7583801/send-mass-emails-with-emailmultialternatives
