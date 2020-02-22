# import numpy as np
import random
import string

from django.contrib.auth.hashers import *
from django.core.management.base import BaseCommand

from auth2.models import *
from rekisteri.models import *


class Command(BaseCommand):

    help = "Tulkkaa se vanha paskakasa"

    def add_arguments(self, parser):
        # parser.add_argument('poll_id', nargs='+', type=int)
        pass

    def handle(self, *args, **options):
        for u in User.objects.all():
            if is_password_usable(u.password):
                print(u.first_name)
                continue
            u.password = "".join(
                random.choice(string.ascii_uppercase + string.digits) for _ in range(32)
            )
            u.save()
