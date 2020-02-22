# import numpy as np

from django.core.management.base import BaseCommand

from auth2.models import *
from rekisteri.models import *


class Command(BaseCommand):

    help = "Tulkkaa se vanha paskakasa"

    def add_arguments(self, parser):
        # parser.add_argument('poll_id', nargs='+', type=int)
        pass

    def handle(self, *args, **options):
        for p in Person.objects.all():
            if p.user.last_login is not None:
                p.dont_publish_in_book = not p.dont_publish_in_book
                p.save()
