from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory, override_settings

from pagetools.core.tests.test_models import ConcretePublishableLangModel
from pagetools.core.views import PaginatorMixin


class CPLMListView(PaginatorMixin):
    model = ConcretePublishableLangModel
    paginate_by = 3


urlpatterns = [
    # custom urlconf
    (r'/', CPLMListView.as_view())
]


@override_settings(ROOT_URLCONF=__name__)
class PaginatorTest(TestCase):

    def setUp(self):
        self.admin = User.objects.create_superuser('admin', 'q@w.de', 'password')
        self.client.login(username="admin", password='password')
        self.factory = RequestFactory()

        for i in range(0, 4):
            ConcretePublishableLangModel.objects.create(foo="f%s" + str(i))

    def test_view(self):
        request = self.factory.get("/")
        v = CPLMListView.as_view()(request)
        self.assertEqual(list(v.context_data['curr_page_range']), list(range(1, 3)))
