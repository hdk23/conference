from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from .models_score import TallyCategoryScore

import numpy as np


# Create your models here.
class Chair(models.Model):
    """
    Chair class that represents committee directors (CDs) and committee managers (CMs)
    Separate classes for CDs and CMs
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, is_staff=True)

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
    user = models.OneToOneField(User)

    def __str__(self):
        return f"Delegate {self.user.get_full_name()}"


class Delegation(models.Model):
    """
    Delegation class that represents a country in a committee
    Assumes that delegates of a delegation are scored together
    Tallies track a delegation's position paper, speech, participation, etc. scores
    """
    country = CountryField()
    delegates = models.ManyToManyField(Delegate)
    tally_category_scores = models.ManyToManyField(TallyCategoryScore)
    score = models.DecimalField(max_digits=5, decimal_places=2)

    def calc_score(self):
        """totals the delegation's scores from each category using a dot product"""
        weights = []
        scores = []
        for tally_category in self.tally_category_scores.all:
            weights.append(tally_category.category.weight / 100)
            scores.append(tally_category.scaled_score)
        self.score = np.dot(weights, scores)

    def __str__(self):
        return f"Delegate of {self.country.name}"

