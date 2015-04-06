from django.test import TestCase
from django.utils.translation import activate
from pagetools.core.models import *



class ConcretePublishableLangModel(PublishableLangModel):
    def __str__(self):
        return "%s:%s" % (self.lang, self.status)


class PublishableLangModelTest(TestCase):

    def setUp(self):
        self.orglang = get_language()
        self.inst_pub_de = ConcretePublishableLangModel.objects.create(status="published", lang="de")
        self.inst_pub_en = ConcretePublishableLangModel.objects.create(status="published", lang="en")
        self.inst_draft_de = ConcretePublishableLangModel.objects.create(status="draft", lang="de")
        self.inst_draft_en = ConcretePublishableLangModel.objects.create(status="draft", lang="en")
        self.inst_pub_nolang = ConcretePublishableLangModel.objects.create(status="published")
        self.inst_draft_nolang = ConcretePublishableLangModel.objects.create(status="draft")

    def tearDown(self):
        activate(self.orglang)

    def test_find_de_active(self):
        activate("de")
        self.assertEqual(len(ConcretePublishableLangModel.public.lfilter()),2)


    def test_find_en__active(self):
        activate("en")
        self.assertEqual(len(ConcretePublishableLangModel.public.lfilter()),2)

    def test_find_de_kwarg(self):
        self.assertEqual(len(ConcretePublishableLangModel.public.lfilter(lang="de")),2)

    def test_find_en_kwarg(self):
        self.assertEqual(len(ConcretePublishableLangModel.public.lfilter(lang="en")),2)

    def test_find_nolang(self):
        activate("fr")
        self.assertEqual(len(ConcretePublishableLangModel.public.lfilter()),1)



