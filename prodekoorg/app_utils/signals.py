from django.db.models.signals import post_delete
from django.dispatch import receiver
from easy_thumbnails.signal_handlers import generate_aliases_global
from easy_thumbnails.signals import saved_file

from alumnirekisteri.rekisteri.models import Person
from lifelonglearning.models import Course
from prodekoorg.app_infoscreen.models import Slide
from prodekoorg.app_membership.models import PendingUser
from prodekoorg.app_poytakirjat.models import Dokumentti
from prodekoorg.app_tiedostot.models import Tiedosto, TiedostoVersio
from prodekoorg.app_vaalit.models import Ehdokas

# Generate thumbnails
saved_file.connect(generate_aliases_global)


@receiver(post_delete, sender=Slide)
def slide_image_delete(sender, instance, **kwargs):
    instance.image.delete(False)


@receiver(post_delete, sender=Course)
def course_banner_delete(sender, instance, **kwargs):
    instance.banner.delete(False)


@receiver(post_delete, sender=Ehdokas)
def ehdokas_pic_delete(sender, instance, **kwargs):
    instance.pic.delete(False)


@receiver(post_delete, sender=PendingUser)
def pendinguser_receipt_delete(sender, instance, **kwargs):
    instance.receipt.delete(False)


@receiver(post_delete, sender=Dokumentti)
def dokumentti_doc_file_delete(sender, instance, **kwargs):
    instance.doc_file.delete(False)


@receiver(post_delete, sender=Tiedosto)
def tiedosto_thumbnail_image_delete(sender, instance, **kwargs):
    instance.thumbnail_image.delete(False)


@receiver(post_delete, sender=TiedostoVersio)
def tiedostoversio_file_delete(sender, instance, **kwargs):
    instance.file.delete(False)


@receiver(post_delete, sender=Person)
def person_picture_delete(sender, instance, **kwargs):
    instance.picture.delete(False)
