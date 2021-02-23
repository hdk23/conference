from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
import numpy as np


# Create your models here.
class Chair(models.Model):
    """
    Chair class that represents committee directors (CDs) and committee managers (CMs)
    Separate classes for CDs and CMs
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Chair {self.user.get_full_name()}"


class CommitteeDirector(models.Model):
    """CD class"""
    chair = models.OneToOneField(Chair, on_delete=models.CASCADE)

    def __str__(self):
        return f"CD {self.chair.user.get_full_name()}"


class CommitteeManager(models.Model):
    """CM class"""
    chair = models.OneToOneField(Chair, on_delete=models.CASCADE)

    def __str__(self):
        return f"CM {self.chair.user.get_full_name()}"


class Delegate(models.Model):
    """
    Delegate class that represents a delegate of a delegation
    Delegate class implemented separated from Delegation class to leave option for double delegation
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Delegate {self.user.get_full_name()}"


class Delegation(models.Model):
    """
    Delegation class that represents a country in a committee
    Assumes that delegates of a delegation are scored together
    Tallies track a delegation's position paper, speech, participation, etc. scores
    Uses the variables present and voting to indicate whether a delegate is present, present & voting, or absent
    """
    country = CountryField()
    delegates = models.ManyToManyField(Delegate)
    present = models.BooleanField(default=True)
    voting = models.BooleanField(default=False)

    def __str__(self):
        if self.voting:
            return f"Delegation of {self.country.name}: Present and Voting"
        elif self.present:
            return f"Delegation of {self.country.name}: Present"
        else:
            return f"Delegation of {self.country.name}: Absent"


class PeopleManager(models.Model):
    directors = models.ManyToManyField(CommitteeDirector)
    managers = models.ManyToManyField(CommitteeManager)
    delegations = models.ManyToManyField(Delegation)
    simple_majority = models.PositiveSmallIntegerField(blank=True, null=True)
    super_majority = models.PositiveSmallIntegerField(blank=True, null=True)

    def calc_votes(self):
        self.simple_majority = self.delegations.all().count() // 2 + 1
        self.super_majority = round(self.delegations.all().count() * 2 / 3)
        self.save()

    def __str__(self):
        return f"People Manager"
