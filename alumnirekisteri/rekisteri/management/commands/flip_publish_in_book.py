#import numpy as np
import json
import django
import csv
import sys
import requests
import re
from pprint import pprint
from django.core.management.base import BaseCommand, CommandError
from rekisteri.models import *
from auth2.models import *
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.core.files.base import ContentFile


class Command(BaseCommand):

    help = 'Tulkkaa se vanha paskakasa'

    def add_arguments(self, parser):
        #parser.add_argument('poll_id', nargs='+', type=int)
        pass

    def handle(self, *args, **options):
        for p in Person.objects.all():
            if(p.user.last_login is not None):
                p.dont_publish_in_book = not p.dont_publish_in_book
                p.save()
