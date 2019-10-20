from alumnirekisteri.rekisteri.models import Person
from django.db.models.signals import post_delete
from django.dispatch import receiver
from lifelonglearning.models import Course
from prodekoorg.app_apply_for_membership.models import PendingUser
from prodekoorg.app_infoscreen.models import Slide
from prodekoorg.app_kulukorvaus.models import Kulukorvaus, KulukorvausPerustiedot
from prodekoorg.app_poytakirjat.models import Dokumentti
from prodekoorg.app_tiedostot.models import Tiedosto, TiedostoVersio
from prodekoorg.app_vaalit.models import Ehdokas


@receiver(post_delete, sender=Slide)
def slide_delete(sender, instance, **kwargs):
    instance.image.delete(False)


@receiver(post_delete, sender=Course)
def slide_delete(sender, instance, **kwargs):
    instance.banner.delete(False)


@receiver(post_delete, sender=Ehdokas)
def slide_delete(sender, instance, **kwargs):
    instance.pic.delete(False)


@receiver(post_delete, sender=PendingUser)
def slide_delete(sender, instance, **kwargs):
    instance.receipt.delete(False)


@receiver(post_delete, sender=KulukorvausPerustiedot)
def slide_delete(sender, instance, **kwargs):
    instance.pdf.delete(False)


@receiver(post_delete, sender=Kulukorvaus)
def slide_delete(sender, instance, **kwargs):
    instance.receipt.delete(False)


@receiver(post_delete, sender=Dokumentti)
def slide_delete(sender, instance, **kwargs):
    instance.doc_file.delete(False)


@receiver(post_delete, sender=Tiedosto)
def slide_delete(sender, instance, **kwargs):
    instance.thumbnail_image.delete(False)


@receiver(post_delete, sender=TiedostoVersio)
def slide_delete(sender, instance, **kwargs):
    instance.file.delete(False)


@receiver(post_delete, sender=Person)
def slide_delete(sender, instance, **kwargs):
    instance.picture.delete(False)
