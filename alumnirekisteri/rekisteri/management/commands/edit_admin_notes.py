import django
import csv
import sys
import requests
from django.core.management.base import BaseCommand, CommandError
from rekisteri.models import *
from auth2.models import *
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.core.files.base import ContentFile


class Command(BaseCommand):

    help = "Import a csv where first column is email, second and third first and last name and fourth is the note to set"

    def add_arguments(self, parser):
        parser.add_argument("path", nargs=1, type=str)
        pass

    def handle(self, *args, **options):
        print("handle")
        with open(options["path"][0]) as notes_file:
            print("opened file")
            notes = csv.reader(notes_file)
            i = 0

            for row in notes:
                # print(row[0], row[1])
                try:
                    user = User.objects.get(email=row[0])
                except:
                    e = sys.exc_info()[0]
                    try:
                        # löyty nimellä, eri email
                        user = User.objects.get(first_name=row[1], last_name=row[2])
                        # print(user.email, row[2])

                        """
                         user.email = row[2]

                         email = Email()
                         email.address = row[3]
                         email.person = user.person
                         email.save()
                         """
                    except:
                        # ei löytynyt emaililla eikä nimellä
                        i += 1
                        e2 = sys.exc_info()[0]
                        print("Didn't find person", row[0], row[1], row[2])
                        continue

                    # print(e, row[3] + " not found")

                if hasattr(user, "person"):
                    user.person.admin_note = row[3]
                    user.person.save()

            print(i)
