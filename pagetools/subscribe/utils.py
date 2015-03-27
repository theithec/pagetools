'''
Created on 03.09.2012

@author: lotek
'''

from django.template.loader import render_to_string
from django.utils.translation import activate, get_language
from pagetools.subscribe import settings as subs_settings

from .models import QueuedEmail, SendStatus


def to_queue(content, **kwargs):
    lang = content.get('lang', None) or kwargs.get('lang', None)
    orglang = get_language()
    if lang:
        activate(lang)
    msg = render_to_string('subscribe/msg.html', {
        'title': content['title'],
        'content': content['body'],
        'site': subs_settings.SUBSCRIBER_URL,
        'unsubscribe_url': subs_settings.SUBSCRIBER_URL
    })
    qm = QueuedEmail(
        subject="%s %s" % (subs_settings.NEWS_SUBJECT_PREFIX, content['title']),
        body=msg
    )
    qm.save(lang=lang)
    activate(orglang)


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

# influenced by:
# http://stackoverflow.com/questions/7583801/send-mass-emails-with-emailmultialternatives
