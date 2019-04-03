#import numpy as np
import json
import django
from pprint import pprint
from django.core.management.base import BaseCommand, CommandError
from rekisteri.models import *
from auth2.models import *


class Command(BaseCommand):

    help = 'Tulkkaa se vanha paskakasa'

    def add_arguments(self, parser):
        #parser.add_argument('poll_id', nargs='+', type=int)
        pass

    def handle(self, *args, **options):
        for p in Person.objects.all():
            p.show_name_category = False
            p.show_address_category = False
            p.show_military_category = False
            p.show_personal_category = False
            p.show_email_address = False
            p.save()
