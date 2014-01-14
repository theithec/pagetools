'''
Created on 14.12.2013

@author: lotek
'''

from django.test import TestCase

from pagetools.gallery.models import Gallery, GalleryPic


class TC1Tests(TestCase):

    def setUp(self):
        self.gal = Gallery.objects.create(title="G1")
        self.pic1 = GalleryPic.objects.create(title='pic1', pic='pic1.jpg')
        
    def test_gal(self):
        print "Gal"
        print self.gal
        print self.pic1
