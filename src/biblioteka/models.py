from django.db import models


# Create your models here.
class CountryState(models.Model):
    state = models.CharField("estado", max_length=100, unique=True)
    abbreviation = models.CharField("sigla", max_length=2, unique=True)
