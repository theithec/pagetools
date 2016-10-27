from django.test import TestCase

from pagetools.subscriptions.templatetags.subscriptions_tags import do_news_subscribtion

class TTTestCase(TestCase):
    def test_subscripton_node(self):
        nsn = do_news_subscribtion(None, None)
        self.assertTrue('name="email"' in nsn.render({}))
