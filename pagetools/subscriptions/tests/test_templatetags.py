from django.test import TestCase

from pagetools.subscriptions.templatetags.subscriptions_tags import do_subscribe_node

class TTTestCase(TestCase):
    def test_subscripton_node(self):
        nsn = do_subscribe_node(None, None)
        self.assertTrue('name="email"' in nsn.render({}))
