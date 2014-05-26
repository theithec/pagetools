'''
Created on 04.09.2012

@author: lotek
'''
from django.core.management.base import BaseCommand

from pagetools.subscribe import utils


class Command(BaseCommand):
    # args = 'test: create test-mail'
    help = 'sending news from queue'

    def handle(self, *args, **options):
        utils.send_max()
