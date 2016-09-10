from django.core.management.base import BaseCommand

from pagetools.subscriptions import utils


class Command(BaseCommand):
    help = 'sending news from queue'

    def handle(self, *args, **options):
        utils.send_max()
