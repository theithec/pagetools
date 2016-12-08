from django.test import TestCase, RequestFactory
from django.views.generic import DetailView
from pagetools.menus.tests import MenuDataTestCase
from pagetools.menus.views import SelectedMenuentriesMixin
from pagetools.core.tests.test_models import ConcretePublishableLangModel


class SelectedMenuentriesMixinTest(MenuDataTestCase):
    '''
    Tests context-data in a Django Mixin like a boss

    https://gist.github.com/dnmellen/6507189
    '''

    class DummyView(SelectedMenuentriesMixin, DetailView):
        '''
        To test get_context_data we need a TemplateView child
        '''

        def __init__(self, *args, **kwargs):
            self.object = ConcretePublishableLangModel.objects.first()
            super(*args, **kwargs)

        model = ConcretePublishableLangModel

        template_name = 'any_template.html'  # TemplateView requires this attribute

    def setUp(self):

        super().setUp()
        pk = ConcretePublishableLangModel
        self.request = RequestFactory().get('/fake-path')

        # Setup request and view.
        self.view = self.DummyView()

    def test_context_data_no_args(self):

        # Prepare initial params
        kwargs = {}

        # Launch Mixin's get_context_data
        context = self.view.get_context_data(**kwargs)
        # Your checkings here
        self.assertEqual(context['menukeys'], ['dummyview'])
