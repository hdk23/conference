from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class TallyCategory(models.Model):
    """Tally Category for scoring delegates"""
    name = models.CharField(max_length=64)
    acronym = models.CharField(max_length=8)
    weight = models.PositiveSmallIntegerField()
    scaled = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.weight}%)"


class CommitteeTallyCategory(models.Model):
    """Committee Tally Category class for tracking committee category averages"""
    category = models.ForeignKey(TallyCategory, on_delete=models.CASCADE)
    average = models.FloatField(blank=True, null=True)
    stdev = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f"{self.category} Committee Tally Category"


class TallyGroup(models.Model):
    """A group of tally categories that reflect the same delegate skill"""
    name = models.CharField(max_length=64)
    acronym = models.CharField(max_length=8)
    categories = models.ManyToManyField(TallyCategory)

    def __str__(self):
        return f"{self.name} ({self.acronym})"
