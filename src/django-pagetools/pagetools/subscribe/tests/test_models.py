from django.test.testcases import TestCase


from pagetools.subscribe.models import Subscriber, QueuedEmail, SendStatus


class TC1Tests(TestCase):

    def setUp(self):
        for e in ('q@w.com', 'w@q.de'):
            Subscriber.objects.create(email=e, is_activated=True)
            
        qm = QueuedEmail.objects.create(subject='test', body='testbody')
        
    def test_stati(self):
        ses = SendStatus.objects.all()
        self.assertEqual(len(SendStatus.objects.all()), 2)
            
        
        

        
