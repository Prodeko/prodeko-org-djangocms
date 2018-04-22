from django.db import models

# Create your models here.
class Toimari(models.Model):

	#Toimareille+hallituslaisille
	etunimi=models.CharField(max_length=30)
	sukunimi=models.CharField(max_length=30)
	virka=models.CharField(max_length=50)
	jaosto=models.CharField(max_length=100)
	# Vain hallituslaisille
	virka_eng=models.CharField(max_length=30, blank=True)
	puhelin=models.CharField(max_length=20, blank=True)
	sahkoposti=models.CharField(max_length=30, blank=True)

	@property
	def name(self):
		return '%s %s' % (self.etunimi, self.sukunimi)

	def __str__(self):
		return self.name + ", " + self.virka

	class Meta:
		verbose_name_plural = "toimarit"