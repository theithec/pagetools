from django.test import TestCase
from django.test.client import Client

from django.core.urlresolvers import resolve, reverse

from django.conf import settings

from pagetools.subscriptions.models import Subscriber

class ViewTest(TestCase):

    def setUp(self):
        self.client = Client()


    def test_subscribeview(self):
        #import pdb; pdb.set_trace()
        settings.DEBUG=True
        u = reverse("subscriptions:subscribe", args=[])
        response = self.client.post(u+"/",
                        {'email': 'q@w.de' }
        )

        subs = Subscriber.objects.all()
        self.assertTrue(len(subs), 1)
