from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime


# Create your models here.
class Chair(models.Model):
    """
    Chair class that represents committee directors (CDs) and committee managers (CMs)
    Separate classes for CDs and CMs
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Chair {self.user.get_full_name()}"


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


class Tally(models.Model):
    """Individual scores for a delegate's position paper, speech, participation, etc."""
    timestamp = models.DateTimeField(auto_now_add=True)
    # scorer = models.ForeignKey(Chair)
    score = models.PositiveSmallIntegerField()
