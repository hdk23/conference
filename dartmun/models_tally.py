from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class TallyCategory(models.Model):
    """Tally Category for scoring delegates"""
    name = models.CharField(max_length=64)
    acronym = models.CharField(max_length=8)
    weight = models.PositiveSmallIntegerField()
    average = models.DecimalField(max_digits=5, decimal_places=3)
    stdev = models.DecimalField(max_digits=5, decimal_places=3)

    def __str__(self):
        return f"{self.name} ({self.weight})%"


class TallyGroup(models.Model):
    """A group of tally categories that reflect the same delegate skill"""
    name = models.CharField(max_length=64)
    acronym = models.CharField(max_length=8)
    categories = models.ManyToManyField(TallyCategory)

    def __str__(self):
        return f"{self.name} ({self.acronym})"
